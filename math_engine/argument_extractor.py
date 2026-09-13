import inspect
import re

from math_engine.language_schema import (
    get_parameter_type,
    get_parameter_aliases,
)

from math_engine.registry import math_registry


NUMBER_PATTERN = r"-?\d+(?:\.\d+)?"

VARIABLE_PATTERN = r"[A-Za-z][A-Za-z0-9_]*"

EXPRESSION_STOP_PATTERNS = [
    r"\bwith respect to\b",
    r"\bwhere\b",
    r"\bwhen\b",
    r"\bat\b",
    r"\bfrom\b",
    r"\bbetween\b",
    r"\bover\b",
    r"\bdirection(?:\s+vector)?\b",
]


RELATION_WORD_REPLACEMENTS = [
    (
        r"\bis less than or equal to\b",
        "<=",
    ),
    (
        r"\bis greater than or equal to\b",
        ">=",
    ),
    (
        r"\bless than or equal to\b",
        "<=",
    ),
    (
        r"\bgreater than or equal to\b",
        ">=",
    ),
    (
        r"\bis not equal to\b",
        "!=",
    ),
    (
        r"\bnot equal to\b",
        "!=",
    ),
    (
        r"\bis equal to\b",
        "=",
    ),
    (
        r"\bequals\b",
        "=",
    ),
]


def _normalize_text(text):
    """
    Normalize text for argument extraction.
    """

    return " ".join(
        str(text)
        .lower()
        .strip()
        .split()
    )


def _extract_number_after_alias(text, alias):
    """
    Extract a number associated with a named parameter alias.

    Supports forms such as:

        radius 7
        radius of 7
        radius is 7
        radius = 7
        width of 5
        height: 10
    """

    escaped_alias = re.escape(alias)

    pattern = (
        rf"\b{escaped_alias}\b"
        rf"\s*(?:of|is|equals|=|:)?\s*"
        rf"({NUMBER_PATTERN})"
    )

    match = re.search(
        pattern,
        text,
        flags=re.IGNORECASE,
    )

    if match is None:
        return None

    number_text = match.group(1)

    if "." in number_text:
        return float(number_text)

    return int(number_text)


def extract_named_number(text, parameter_name):
    """
    Find a numeric value for a specific parameter using
    its known natural-language aliases.
    """

    normalized_text = _normalize_text(text)

    aliases = get_parameter_aliases(
        parameter_name
    )

    # Longer aliases should be checked first.
    aliases = sorted(
        aliases,
        key=len,
        reverse=True,
    )

    for alias in aliases:

        value = _extract_number_after_alias(
            normalized_text,
            alias,
        )

        if value is not None:
            return value

    return None


def _clean_extracted_text(value):
    """
    Clean punctuation and whitespace from extracted symbolic
    text without changing the mathematical content.
    """

    if value is None:
        return None

    value = str(value).strip()

    value = value.rstrip(
        ".,?!;"
    ).strip()

    if not value:
        return None

    return value


def _extract_named_text(text, alias):
    """
    Extract text associated with a named parameter.

    Examples:

        expression x**2 + 3*x
        expression is x**2
        equation: x + 2 = 5
        function = sin(x)
    """

    escaped_alias = re.escape(
        alias
    )

    stop_pattern = "|".join(
        EXPRESSION_STOP_PATTERNS
    )

    pattern = (
        rf"\b{escaped_alias}\b"
        rf"\s*(?:of|is|equals|=|:)?\s*"
        rf"(.+?)"
        rf"(?="
        rf"{stop_pattern}"
        rf"|[,;]"
        rf"|$"
        rf")"
    )

    match = re.search(
        pattern,
        str(text),
        flags=re.IGNORECASE,
    )

    if match is None:
        return None

    return _clean_extracted_text(
        match.group(1)
    )


def extract_named_expression(
    text,
    parameter_name,
):
    """
    Extract a symbolic expression using the parameter's
    known aliases.
    """

    aliases = get_parameter_aliases(
        parameter_name
    )

    aliases = sorted(
        aliases,
        key=len,
        reverse=True,
    )

    for alias in aliases:

        value = _extract_named_text(
            text,
            alias,
        )

        if value is not None:
            return value

    return None


def extract_variable(
    text,
    parameter_name="variable",
):
    """
    Extract a mathematical variable.

    Supports forms such as:

        variable x
        variable is x
        variable = x
        with respect to x
        in terms of x
    """

    text = str(text)

    # --------------------------------------------------------
    # NAMED VARIABLE
    # --------------------------------------------------------

    aliases = get_parameter_aliases(
        parameter_name
    )

    aliases = sorted(
        aliases,
        key=len,
        reverse=True,
    )

    for alias in aliases:

        escaped_alias = re.escape(
            alias
        )

        pattern = (
            rf"\b{escaped_alias}\b"
            rf"\s*(?:is|equals|=|:)?\s*"
            rf"({VARIABLE_PATTERN})\b"
        )

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match is not None:
            return match.group(1)

    # --------------------------------------------------------
    # CALCULUS / ALGEBRA LANGUAGE
    # --------------------------------------------------------

    patterns = [
        rf"\bwith respect to\s+({VARIABLE_PATTERN})\b",
        rf"\bin terms of\s+({VARIABLE_PATTERN})\b",
        rf"\bsolve for\s+({VARIABLE_PATTERN})\b",
        rf"\bfor\s+({VARIABLE_PATTERN})\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match is not None:
            return match.group(1)

    return None


def extract_expression(
    text,
    parameter_name="expression",
):
    """
    Extract a symbolic mathematical expression.

    First tries explicit named parameters such as:

        expression x**2 + 3*x

    Then handles common mathematical language such as:

        derivative of x**3 with respect to x
        differentiate x**2 with respect to x
        integrate sin(x) with respect to x
        simplify x**2 + 2*x + 1
        factor x**2 - 4
        expand (x + 1)**2
    """

    # --------------------------------------------------------
    # LEFT / RIGHT SIDE OF AN EQUATION
    # --------------------------------------------------------
    #
    # Some deterministic algebra functions use signatures such
    # as:
    #
    #     solve_equation(left_side, right_side=0, variable="x")
    #
    # rather than accepting one combined "equation" argument.
    # --------------------------------------------------------

    if parameter_name in {
        "left_side",
        "right_side",
    }:

        normalized_relation = (
            _normalize_relation_words(
                text
            )
        )

        # Remove common command language.
        normalized_relation = re.sub(
            r"^\s*solve\s+(?:the\s+)?equation\s*[:=]?\s*",
            "",
            normalized_relation,
            count=1,
            flags=re.IGNORECASE,
        )

        normalized_relation = re.sub(
            r"^\s*solve\s+",
            "",
            normalized_relation,
            count=1,
            flags=re.IGNORECASE,
        )

        # Remove a trailing "for x".
        normalized_relation = re.sub(
            rf"\s+for\s+{VARIABLE_PATTERN}"
            rf"\s*[.?!;]*$",
            "",
            normalized_relation,
            flags=re.IGNORECASE,
        )

        relation_match = re.search(
            r"(.+?)\s*(<=|>=|!=|==|=|<|>)\s*(.+)",
            normalized_relation,
        )

        if relation_match is not None:

            if parameter_name == "left_side":
                return _clean_extracted_text(
                    relation_match.group(1)
                )

            if parameter_name == "right_side":

                right_side = _clean_extracted_text(
                    relation_match.group(3)
                )

                if right_side is not None:
                    right_side = re.split(
                        r"\s+(?:from|between)\s+",
                        right_side,
                        maxsplit=1,
                        flags=re.IGNORECASE,
                    )[0]

                return _clean_extracted_text(
                    right_side
                )

    # --------------------------------------------------------
    # DIRECTIONAL DERIVATIVE
    # --------------------------------------------------------
    #
    # Example:
    #
    #     Find the directional derivative of x**2 + y**2
    #     direction (1, 1)
    #
    # Extract only:
    #
    #     x**2 + y**2
    # --------------------------------------------------------

    directional_match = re.search(
        r"\bdirectional\s+derivative\s+of\s+(.+?)"
        r"\s+(?:in\s+the\s+)?direction(?:\s+vector)?\s*"
        r"(?:is|=|:)?\s*\(",
        str(text),
        flags=re.IGNORECASE,
    )

    if directional_match is not None:
        return _clean_extracted_text(
            directional_match.group(1)
        )

    # --------------------------------------------------------
    # EXPLICITLY NAMED EXPRESSION
    # --------------------------------------------------------

    value = extract_named_expression(
        text,
        parameter_name,
    )

    if value is not None:
        return value

    text = str(text).strip()

    # --------------------------------------------------------
    # "DERIVATIVE OF ..."
    # "INTEGRAL OF ..."
    # --------------------------------------------------------

    patterns = [
        r"\bderivative\s+of\s+(.+?)(?=\s+with respect to\b|$)",
        (
            r"\bintegral\s+of\s+(.+?)"
            r"(?=\s+(?:from|between)\b|\s+with respect to\b|$)"
        ),
        r"\bdifferentiate\s+(.+?)(?=\s+with respect to\b|$)",
        (
            r"\bintegrate\s+(.+?)"
            r"(?=\s+(?:from|between)\b|\s+with respect to\b|$)"
        ),
        r"\bsimplify\s+(.+)$",
        r"\bfactor\s+(.+)$",
        r"\bexpand\s+(.+)$",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match is not None:
            return _clean_extracted_text(
                match.group(1)
            )

    return None


def _normalize_relation_words(text):
    """
    Convert common natural-language mathematical relations
    into symbolic operators.

    Examples:

        x equals 5
            -> x = 5

        x is less than or equal to 7
            -> x <= 7
    """

    text = str(text)

    for pattern, replacement in (
        RELATION_WORD_REPLACEMENTS
    ):

        text = re.sub(
            pattern,
            replacement,
            text,
            flags=re.IGNORECASE,
        )

    return text


def _contains_relation_operator(text):
    """
    Return True if text contains a mathematical relation
    operator suitable for an equation or inequality.
    """

    return re.search(
        r"(<=|>=|!=|==|=|<|>)",
        str(text),
    ) is not None


def extract_equation(
    text,
    parameter_name="equation",
):
    """
    Extract an equation or inequality from natural language.

    Supports forms such as:

        Solve 2*x + 3 = 11 for x.

        Solve the equation x + 5 = 12.

        equation x**2 - 4 = 0

        x + 5 equals 12

        inequality 2*x + 1 <= 7
    """

    text = _normalize_relation_words(
        text
    )

    text = str(text).strip()

    # --------------------------------------------------------
    # REMOVE COMMON COMMAND PREFIXES
    # --------------------------------------------------------

    prefix_patterns = [
        r"^\s*solve\s+(?:the\s+)?equation\s*[:=]?\s*",
        r"^\s*solve\s+(?:the\s+)?inequality\s*[:=]?\s*",
        r"^\s*solve\s+",
        r"^\s*equation\s*(?:is|:)?\s*",
        r"^\s*inequality\s*(?:is|:)?\s*",
    ]

    for pattern in prefix_patterns:

        new_text = re.sub(
            pattern,
            "",
            text,
            count=1,
            flags=re.IGNORECASE,
        )

        if new_text != text:
            text = new_text
            break

    # --------------------------------------------------------
    # REMOVE TRAILING "FOR x"
    # --------------------------------------------------------
    #
    # Example:
    #
    #     2*x + 3 = 11 for x
    #
    # becomes:
    #
    #     2*x + 3 = 11
    # --------------------------------------------------------

    text = re.sub(
        rf"\s+for\s+{VARIABLE_PATTERN}"
        rf"\s*[.?!;]*$",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = _clean_extracted_text(
        text
    )

    if text is None:
        return None

    # --------------------------------------------------------
    # VALIDATE THAT WE ACTUALLY FOUND A RELATION
    # --------------------------------------------------------

    if not _contains_relation_operator(
        text
    ):
        return None

    return text


def _equation_to_zero_expression(equation):
    """
    Convert an equation into an expression assumed equal to zero.

    Example:

        x + y = 5

    becomes:

        (x + y) - (5)

    This matches the input format expected by SATURN's
    deterministic system-solving functions.
    """

    equation = _normalize_relation_words(
        equation
    )

    match = re.match(
        r"^\s*(.+?)\s*=\s*(.+?)\s*$",
        str(equation),
    )

    if match is None:
        return _clean_extracted_text(
            equation
        )

    left_side = _clean_extracted_text(
        match.group(1)
    )

    right_side = _clean_extracted_text(
        match.group(2)
    )

    if (
        left_side is None
        or right_side is None
    ):
        return None

    return (
        f"({left_side}) - "
        f"({right_side})"
    )


def extract_equation_list(
    text,
    parameter_name="equations",
):
    """
    Extract multiple equations from a natural-language
    system-of-equations request.

    Each equation is converted to SATURN's system-solver
    representation:

        left = right

    becomes:

        (left) - (right)

    Supports equations separated by:

        newlines
        semicolons
    """

    text = _normalize_relation_words(
        text
    )

    text = str(text).strip()

    # --------------------------------------------------------
    # REMOVE SYSTEM COMMAND LANGUAGE
    # --------------------------------------------------------

    text = re.sub(
        (
            r"^\s*solve\s+(?:the\s+)?"
            r"(?:following\s+)?system"
            r"(?:\s+of\s+equations)?"
            r"\s*[:\-]?\s*"
        ),
        "",
        text,
        count=1,
        flags=re.IGNORECASE,
    )

    # --------------------------------------------------------
    # REMOVE TRAILING VARIABLE REQUEST
    # --------------------------------------------------------
    #
    # Example:
    #
    #     for x and y
    #
    # --------------------------------------------------------

    text = re.sub(
        (
            r"\s+for\s+"
            r"[A-Za-z][A-Za-z0-9_]*"
            r"(?:\s*(?:,|and)\s*"
            r"[A-Za-z][A-Za-z0-9_]*)*"
            r"\s*[.?!]*$"
        ),
        "",
        text,
        flags=re.IGNORECASE,
    )

    # --------------------------------------------------------
    # SPLIT THE SYSTEM
    # --------------------------------------------------------

    pieces = re.split(
        r"(?:\r?\n|;)+",
        text,
    )

    equations = []

    for piece in pieces:

        piece = _clean_extracted_text(
            piece
        )

        if piece is None:
            continue

        if not _contains_relation_operator(
            piece
        ):
            continue

        equation = _equation_to_zero_expression(
            piece
        )

        if equation is not None:
            equations.append(
                equation
            )

    if not equations:
        return None

    return equations


def extract_variable_list(
    text,
    parameter_name="variables",
):
    """
    Extract multiple mathematical variables.

    Supports forms such as:

        for x and y
        for x, y
        for x, y, and z
        variables x and y
        variables x, y, z
    """

    text = str(text)

    # --------------------------------------------------------
    # FIND THE VARIABLE PORTION
    # --------------------------------------------------------

    patterns = [
        r"\bfor\s+(.+?)\s*[.?!;]*$",
        (
            r"\bvariables?\s*"
            r"(?:are|:|=)?\s*"
            r"(.+?)\s*[.?!;]*$"
        ),
    ]

    variable_text = None

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match is not None:

            variable_text = match.group(1)

            break

    if variable_text is None:
        return None

    # --------------------------------------------------------
    # NORMALIZE LIST SEPARATORS
    # --------------------------------------------------------
    #
    # Examples:
    #
    #     x and y
    #         -> x,y
    #
    #     x, y, and z
    #         -> x,y,z
    #
    # --------------------------------------------------------

    variable_text = re.sub(
        r"\s*,\s*and\s+",
        ",",
        variable_text,
        flags=re.IGNORECASE,
    )

    variable_text = re.sub(
        r"\s+and\s+",
        ",",
        variable_text,
        flags=re.IGNORECASE,
    )

    pieces = re.split(
        r"\s*,\s*",
        variable_text,
    )

    variables = []

    for piece in pieces:

        variable = piece.strip()

        if re.fullmatch(
            VARIABLE_PATTERN,
            variable,
        ):

            if variable not in variables:
                variables.append(
                    variable
                )

    if not variables:
        return None

    return variables


def _parse_coordinate_values(value):
    """
    Parse comma-separated coordinate/vector components.

    Examples:

        "3, 4"       -> [3, 4]
        "1, -2, 5"   -> [1, -2, 5]
        "x, y + 1"   -> ["x", "y + 1"]

    Numeric components are converted to int/float when
    possible. Symbolic components remain strings.
    """

    pieces = [
        piece.strip()
        for piece in str(value).split(",")
    ]

    if len(pieces) < 2:
        return None

    result = []

    for piece in pieces:

        if not piece:
            return None

        if re.fullmatch(
            NUMBER_PATTERN,
            piece,
        ):
            number = float(piece)

            if number.is_integer():
                number = int(number)

            result.append(number)

        else:
            result.append(piece)

    return result


def extract_point(
    text,
    parameter_name="point",
):
    """
    Extract a mathematical point.

    Supports forms such as:

        point (3, 4)
        point = (3, 4)
        at (3, 4)
        start point (1, 2, 3)
        end point (4, 5, 6)
    """

    text = str(text)

    aliases = get_parameter_aliases(
        parameter_name
    )

    # --------------------------------------------------------
    # NAMED POINT
    # --------------------------------------------------------

    for alias in aliases:

        pattern = (
            rf"\b{re.escape(alias)}\b"
            rf"\s*(?:is|=|:)?\s*"
            rf"\(([^()]+)\)"
        )

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match is not None:

            return _parse_coordinate_values(
                match.group(1)
            )

    # --------------------------------------------------------
    # GENERIC "AT (x, y)"
    # --------------------------------------------------------

    if parameter_name == "point":

        match = re.search(
            r"\bat\s*\(([^()]+)\)",
            text,
            flags=re.IGNORECASE,
        )

        if match is not None:

            return _parse_coordinate_values(
                match.group(1)
            )

    return None


def extract_vector(
    text,
    parameter_name="vector",
):
    """
    Extract a mathematical vector.

    Supports forms such as:

        vector (3, 4)
        vector = (3, 4)
        direction (1, -2)
        direction vector (1, -2, 3)
    """

    text = str(text)

    aliases = get_parameter_aliases(
        parameter_name
    )

    for alias in aliases:

        pattern = (
            rf"\b{re.escape(alias)}\b"
            rf"\s*(?:vector\s*)?"
            rf"(?:is|=|:)?\s*"
            rf"\(([^()]+)\)"
        )

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match is not None:

            return _parse_coordinate_values(
                match.group(1)
            )

    return None



def _parse_bound_value(value):
    """
    Parse one bound value.

    Numeric values become int/float. Symbolic values such as
    pi, -pi, oo, a, or 2*pi remain strings for the deterministic
    SymPy-backed subsystem to interpret.
    """

    value = _clean_extracted_text(
        value
    )

    if value is None:
        return None

    if re.fullmatch(
        NUMBER_PATTERN,
        value,
    ):
        number = float(value)

        if number.is_integer():
            return int(number)

        return number

    return value


def _clean_bound_value_text(value):
    """
    Remove trailing command language that is not part of a bound.

    Example:

        "5 with respect to x"
            -> "5"
    """

    if value is None:
        return None

    value = re.split(
        (
            r"\s+(?:with\s+respect\s+to|"
            r"where|using|for)\b"
        ),
        str(value),
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]

    return _clean_extracted_text(
        value
    )


def _extract_bound_pair(text, prefix=None):
    """
    Extract a two-value interval/bound pair.

    Supported forms include:

        from 0 to 5
        between -2 and 4
        x from 0 to 2
        y between -1 and 1
        interval (0, 5)
        x bounds (0, 2)
    """

    text = str(text)

    if prefix is None:
        prefix_pattern = ""
    else:
        prefix_pattern = (
            rf"\b{re.escape(prefix)}\b\s*"
        )

    patterns = [
        (
            prefix_pattern
            + r"(?:from\s+)"
            + r"(.+?)\s+to\s+(.+?)"
            + r"(?=\s+(?:with\s+respect\s+to|where|using|for)\b|[.?!;]|$)"
        ),
        (
            prefix_pattern
            + r"(?:between\s+)"
            + r"(.+?)\s+and\s+(.+?)"
            + r"(?=\s+(?:with\s+respect\s+to|where|using|for)\b|[.?!;]|$)"
        ),
        (
            prefix_pattern
            + r"(?:bounds?|limits?|interval)?\s*"
            + r"(?:is|=|:)?\s*"
            + r"[\(\[]\s*([^,\]\)]+)\s*,\s*([^,\]\)]+)\s*[\)\]]"
        ),
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match is None:
            continue

        lower_text = _clean_bound_value_text(
            match.group(1)
        )

        upper_text = _clean_bound_value_text(
            match.group(2)
        )

        lower = _parse_bound_value(
            lower_text
        )

        upper = _parse_bound_value(
            upper_text
        )

        if (
            lower is not None
            and upper is not None
        ):
            return (
                lower,
                upper,
            )

    return None


def extract_bounds(
    text,
    parameter_name="interval",
):
    """
    Extract lower/upper limits or a complete interval.

    Individual parameters:
        lower
        upper
        lower_bound
        upper_bound

    Pair parameters:
        interval
        x_bounds
        y_bounds
        z_bounds
        r_bounds
        theta_bounds
    """

    parameter_name = str(
        parameter_name
    ).lower()

    # --------------------------------------------------------
    # INDIVIDUAL LOWER / UPPER PARAMETERS
    # --------------------------------------------------------

    if parameter_name in {
        "lower",
        "lower_bound",
        "upper",
        "upper_bound",
    }:

        # First support explicit language such as:
        #
        #     lower bound 0
        #     upper limit pi

        aliases = sorted(
            get_parameter_aliases(
                parameter_name
            ),
            key=len,
            reverse=True,
        )

        for alias in aliases:

            # "from" and "to" are handled more safely as a pair
            # below because "to" can appear in unrelated language.
            if alias.lower() in {
                "from",
                "to",
            }:
                continue

            match = re.search(
                (
                    rf"\b{re.escape(alias)}\b"
                    rf"\s*(?:is|=|:)?\s*"
                    rf"(.+?)"
                    rf"(?=\s+(?:upper|lower|with\s+respect\s+to|"
                    rf"where|using|for)\b|[,;]|$)"
                ),
                str(text),
                flags=re.IGNORECASE,
            )

            if match is not None:

                value = _parse_bound_value(
                    _clean_bound_value_text(
                        match.group(1)
                    )
                )

                if value is not None:
                    return value

        pair = _extract_bound_pair(
            text
        )

        if pair is None:
            return None

        if parameter_name in {
            "lower",
            "lower_bound",
        }:
            return pair[0]

        return pair[1]

    # --------------------------------------------------------
    # NAMED MULTI-DIMENSIONAL BOUNDS
    # --------------------------------------------------------

    prefix_map = {
        "x_bounds": "x",
        "y_bounds": "y",
        "z_bounds": "z",
        "r_bounds": "r",
        "theta_bounds": "theta",
    }

    if parameter_name in prefix_map:

        prefix = prefix_map[
            parameter_name
        ]

        pair = _extract_bound_pair(
            text,
            prefix=prefix,
        )

        if pair is not None:
            return pair

        # Also support:
        #
        #     x bounds (0, 2)

        named_patterns = [
            rf"\b{re.escape(prefix)}\s+bounds?\b",
            rf"\b{re.escape(prefix)}\s+limits?\b",
        ]

        for named_prefix in named_patterns:

            match = re.search(
                (
                    named_prefix
                    + r"\s*(?:is|=|:)?\s*"
                    + r"[\(\[]\s*([^,\]\)]+)\s*,\s*"
                    + r"([^,\]\)]+)\s*[\)\]]"
                ),
                str(text),
                flags=re.IGNORECASE,
            )

            if match is not None:

                return (
                    _parse_bound_value(
                        match.group(1)
                    ),
                    _parse_bound_value(
                        match.group(2)
                    ),
                )

        return None

    # --------------------------------------------------------
    # GENERIC INTERVAL
    # --------------------------------------------------------

    if parameter_name == "interval":

        pair = _extract_bound_pair(
            text
        )

        if pair is not None:
            return pair

        aliases = get_parameter_aliases(
            parameter_name
        )

        for alias in aliases:

            match = re.search(
                (
                    rf"\b{re.escape(alias)}\b"
                    rf"\s*(?:is|=|:)?\s*"
                    rf"[\(\[]\s*([^,\]\)]+)\s*,\s*"
                    rf"([^,\]\)]+)\s*[\)\]]"
                ),
                str(text),
                flags=re.IGNORECASE,
            )

            if match is not None:

                return (
                    _parse_bound_value(
                        match.group(1)
                    ),
                    _parse_bound_value(
                        match.group(2)
                    ),
                )

    return None



def _split_top_level_commas(value):
    """
    Split comma-separated text while respecting nested (), [], and {}.

    Examples:

        "3, 4, 5"
            -> ["3", "4", "5"]

        "(0, 0), (4, 0), (4, 3)"
            -> ["(0, 0)", "(4, 0)", "(4, 3)"]
    """

    value = str(value)

    pieces = []
    current = []
    depth = 0

    opening = {
        "(": ")",
        "[": "]",
        "{": "}",
    }

    closing = set(
        opening.values()
    )

    for character in value:

        if character in opening:
            depth += 1

        elif character in closing:
            depth = max(
                0,
                depth - 1,
            )

        if (
            character == ","
            and depth == 0
        ):
            piece = "".join(
                current
            ).strip()

            if piece:
                pieces.append(
                    piece
                )

            current = []
            continue

        current.append(
            character
        )

    final_piece = "".join(
        current
    ).strip()

    if final_piece:
        pieces.append(
            final_piece
        )

    return pieces


def _parse_generic_list_item(value):
    """
    Parse one generic list item.

    Numbers become int/float.
    Coordinate tuples become lists.
    Symbolic expressions remain strings.
    """

    value = _clean_extracted_text(
        value
    )

    if value is None:
        return None

    if re.fullmatch(
        NUMBER_PATTERN,
        value,
    ):
        number = float(value)

        if number.is_integer():
            return int(number)

        return number

    # Coordinate / tuple-like item.
    if (
        value.startswith("(")
        and value.endswith(")")
    ):
        coordinate_value = (
            value[1:-1]
        )

        parsed_coordinates = (
            _parse_coordinate_values(
                coordinate_value
            )
        )

        if parsed_coordinates is not None:
            return parsed_coordinates

    return value


def _parse_generic_list(value):
    """
    Parse list content into structured Python values.

    Examples:

        "3, 4, 5"
            -> [3, 4, 5]

        "x**2, y**2, z**2"
            -> ["x**2", "y**2", "z**2"]

        "(0, 0), (4, 0), (4, 3)"
            -> [[0, 0], [4, 0], [4, 3]]
    """

    value = str(value).strip()

    if (
        len(value) >= 2
        and value[0] in "[{"
        and value[-1] in "]}"
    ):
        value = value[1:-1].strip()

    if not value:
        return None

    pieces = _split_top_level_commas(
        value
    )

    if not pieces:
        return None

    result = []

    for piece in pieces:

        parsed_item = (
            _parse_generic_list_item(
                piece
            )
        )

        if parsed_item is None:
            return None

        result.append(
            parsed_item
        )

    return result


def extract_list(
    text,
    parameter_name="values",
):
    """
    Extract a generic list or component sequence.

    Supported forms include:

        components [3, 4]
        components [x**2, y**2, z**2]
        side lengths [3, 4, 5]
        points [(0, 0), (4, 0), (4, 3)]

    For recognized component/list parameters, SATURN also accepts
    parenthesized component sequences such as:

        components (3, 4)
    """

    text = str(text)

    aliases = sorted(
        get_parameter_aliases(
            parameter_name
        ),
        key=len,
        reverse=True,
    )

    for alias in aliases:

        escaped_alias = re.escape(
            alias
        )

        # ----------------------------------------------------
        # BRACKETED LIST
        # ----------------------------------------------------

        match = re.search(
            (
                rf"\b{escaped_alias}\b"
                rf"\s*(?:are|is|=|:)?\s*"
                rf"\[([^\]]+)\]"
            ),
            text,
            flags=re.IGNORECASE,
        )

        if match is not None:

            return _parse_generic_list(
                match.group(1)
            )

        # ----------------------------------------------------
        # LIST OF POINTS / NESTED TUPLES
        # ----------------------------------------------------
        #
        # Example:
        #
        #     points [(0, 0), (4, 0), (4, 3)]
        #
        # The bracketed rule above already captures this form.
        # This branch supports an unbracketed sequence:
        #
        #     points (0, 0), (4, 0), (4, 3)
        # ----------------------------------------------------

        if parameter_name == "points":

            match = re.search(
                (
                    rf"\b{escaped_alias}\b"
                    rf"\s*(?:are|is|=|:)?\s*"
                    rf"((?:\([^()]+\)"
                    rf"(?:\s*,\s*|$))+)"
                ),
                text,
                flags=re.IGNORECASE,
            )

            if match is not None:

                return _parse_generic_list(
                    match.group(1)
                )

        # ----------------------------------------------------
        # PARENTHESIZED COMPONENT LIST
        # ----------------------------------------------------

        match = re.search(
            (
                rf"\b{escaped_alias}\b"
                rf"\s*(?:are|is|=|:)?\s*"
                rf"\(([^()]+)\)"
            ),
            text,
            flags=re.IGNORECASE,
        )

        if match is not None:

            return _parse_generic_list(
                match.group(1)
            )

    return None



def _parse_mapping_value(value):
    """
    Parse one mapping/substitution value.

    Numbers become int/float. Symbolic expressions remain strings.
    """

    value = _clean_extracted_text(
        value
    )

    if value is None:
        return None

    if re.fullmatch(
        NUMBER_PATTERN,
        value,
    ):
        number = float(value)

        if number.is_integer():
            return int(number)

        return number

    return value


def extract_mapping(
    text,
    parameter_name="substitutions",
):
    """
    Extract variable/value mappings from natural language.

    Supported forms include:

        substitute x = 2
        substitute x = 2 and y = 3
        substitutions x = 2, y = 3
        replace x with 2 and y with 3

    Returns:

        {"x": 2, "y": 3}
    """

    text = str(text)

    mapping = {}

    # --------------------------------------------------------
    # "x = value" STYLE
    # --------------------------------------------------------

    equals_pattern = (
        rf"\b({VARIABLE_PATTERN})\b"
        rf"\s*=\s*"
        rf"(.+?)"
        rf"(?="
        rf"\s*(?:,|;|\band\b)\s*"
        rf"{VARIABLE_PATTERN}\s*="
        rf"|\s+\b(?:into|in)\b"
        rf"|[.?!;]"
        rf"|$"
        rf")"
    )

    for match in re.finditer(
        equals_pattern,
        text,
        flags=re.IGNORECASE,
    ):

        variable = match.group(1)

        value = _parse_mapping_value(
            match.group(2)
        )

        if value is not None:
            mapping[variable] = value

    if mapping:
        return mapping

    # --------------------------------------------------------
    # "x WITH value" STYLE
    # --------------------------------------------------------

    with_pattern = (
        rf"\b({VARIABLE_PATTERN})\b"
        rf"\s+with\s+"
        rf"(.+?)"
        rf"(?="
        rf"\s*(?:,|;|\band\b)\s*"
        rf"{VARIABLE_PATTERN}\s+with\s+"
        rf"|\s+\b(?:into|in)\b"
        rf"|[.?!;]"
        rf"|$"
        rf")"
    )

    for match in re.finditer(
        with_pattern,
        text,
        flags=re.IGNORECASE,
    ):

        variable = match.group(1)

        value = _parse_mapping_value(
            match.group(2)
        )

        if value is not None:
            mapping[variable] = value

    if mapping:
        return mapping

    return None



def _normalize_option_value(value):
    """
    Normalize a plain-language string/enum option.

    This intentionally does not perform mathematical calculation.
    It only converts common natural-language option spellings into
    deterministic values expected by SATURN's math subsystems.
    """

    value = _clean_extracted_text(
        value
    )

    if value is None:
        return None

    normalized = str(value).strip().lower()

    option_aliases = {
        "degree": "degrees",
        "degrees": "degrees",
        "deg": "degrees",
        "radian": "radians",
        "radians": "radians",
        "rad": "radians",
        "true": True,
        "yes": True,
        "on": True,
        "false": False,
        "no": False,
        "off": False,
    }

    return option_aliases.get(
        normalized,
        value,
    )


def extract_string(
    text,
    parameter_name,
):
    """
    Extract a string/enum-style parameter.

    Supported examples include:

        unit degrees
        unit is radians
        output unit degrees
        function name sin
        solve for rate x
    """

    text = str(text)

    aliases = sorted(
        get_parameter_aliases(
            parameter_name
        ),
        key=len,
        reverse=True,
    )

    for alias in aliases:

        escaped_alias = re.escape(
            alias
        )

        pattern = (
            rf"\b{escaped_alias}\b"
            rf"\s*(?:is|=|:)?\s*"
            rf"([A-Za-z_+\-]+)"
        )

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match is not None:

            return _normalize_option_value(
                match.group(1)
            )

    # --------------------------------------------------------
    # NATURAL ANGLE-UNIT LANGUAGE
    # --------------------------------------------------------

    if parameter_name in {
        "unit",
        "output_unit",
    }:

        unit_match = re.search(
            r"\b(degrees?|deg|radians?|rad)\b",
            text,
            flags=re.IGNORECASE,
        )

        if unit_match is not None:

            return _normalize_option_value(
                unit_match.group(1)
            )

    return None


def extract_boolean(
    text,
    parameter_name,
):
    """
    Extract a boolean option from natural language.

    Supported examples include:

        decimal true
        decimal false
        decimal yes
        decimal no
        as decimal
        without decimal
    """

    text = str(text)

    aliases = sorted(
        get_parameter_aliases(
            parameter_name
        ),
        key=len,
        reverse=True,
    )

    for alias in aliases:

        escaped_alias = re.escape(
            alias
        )

        # Explicit true/false style.
        match = re.search(
            (
                rf"\b{escaped_alias}\b"
                rf"\s*(?:is|=|:)?\s*"
                rf"(true|false|yes|no|on|off)\b"
            ),
            text,
            flags=re.IGNORECASE,
        )

        if match is not None:

            return bool(
                _normalize_option_value(
                    match.group(1)
                )
            )

    # --------------------------------------------------------
    # NATURAL BOOLEAN PHRASES
    # --------------------------------------------------------

    if parameter_name == "decimal":

        negative_patterns = [
            r"\bwithout\s+(?:a\s+)?decimal\b",
            r"\bno\s+decimal\b",
            r"\bdo\s+not\s+(?:use|show|return)\s+(?:a\s+)?decimal\b",
            r"\bnot\s+(?:as\s+)?(?:a\s+)?decimal\b",
        ]

        for pattern in negative_patterns:

            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            ):
                return False

        positive_patterns = [
            r"\bas\s+(?:a\s+)?decimal\b",
            r"\bin\s+decimal(?:\s+form)?\b",
            r"\bdecimal\s+(?:form|answer|result|output)\b",
        ]

        for pattern in positive_patterns:

            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            ):
                return True

    return None



def _extract_coordinate_tuples(text):
    """
    Extract coordinate tuples in the order they appear.

    Examples:

        "(1, 2) and (4, 6)"
            -> [[1, 2], [4, 6]]

        "points (0, 0), (4, 0), (4, 3)"
            -> [[0, 0], [4, 0], [4, 3]]
    """

    matches = re.findall(
        r"\(([^()]+)\)",
        str(text),
    )

    coordinates = []

    for match in matches:

        parsed = _parse_coordinate_values(
            match
        )

        if parsed is not None:
            coordinates.append(
                parsed
            )

    return coordinates


def extract_coordinate_arguments(
    text,
    parameter_names,
):
    """
    Adapt point-style natural language to scalar coordinate
    signatures used by many deterministic geometry functions.

    Examples:

        parameters:
            x1, y1, x2, y2

        text:
            points (1, 2) and (4, 6)

        result:
            {
                "x1": 1,
                "y1": 2,
                "x2": 4,
                "y2": 6,
            }

    The adapter is signature-driven rather than operation-specific.
    """

    parameter_names = list(
        parameter_names
    )

    parameter_set = set(
        parameter_names
    )

    points = _extract_coordinate_tuples(
        text
    )

    arguments = {}

    # --------------------------------------------------------
    # NUMBERED 2D POINT SIGNATURES
    # --------------------------------------------------------
    #
    # Supports:
    #     x1, y1
    #     x1, y1, x2, y2
    #     x1, y1, x2, y2, x3, y3
    # --------------------------------------------------------

    for index in range(
        1,
        len(points) + 1,
    ):

        x_name = f"x{index}"
        y_name = f"y{index}"

        if (
            x_name in parameter_set
            and y_name in parameter_set
            and len(points[index - 1]) >= 2
        ):
            arguments[x_name] = (
                points[index - 1][0]
            )
            arguments[y_name] = (
                points[index - 1][1]
            )

    # --------------------------------------------------------
    # GENERIC x, y SIGNATURE
    # --------------------------------------------------------

    if (
        "x" in parameter_set
        and "y" in parameter_set
        and points
        and len(points[0]) >= 2
    ):
        arguments.setdefault(
            "x",
            points[0][0],
        )
        arguments.setdefault(
            "y",
            points[0][1],
        )

    # --------------------------------------------------------
    # point_x, point_y SIGNATURE
    # --------------------------------------------------------

    if (
        "point_x" in parameter_set
        and "point_y" in parameter_set
        and points
        and len(points[0]) >= 2
    ):
        arguments.setdefault(
            "point_x",
            points[0][0],
        )
        arguments.setdefault(
            "point_y",
            points[0][1],
        )

    # --------------------------------------------------------
    # center_x, center_y SIGNATURE
    # --------------------------------------------------------

    if (
        "center_x" in parameter_set
        and "center_y" in parameter_set
        and points
        and len(points[0]) >= 2
    ):

        center_match = re.search(
            r"\bcenter\b\s*(?:is|=|:)?\s*\(([^()]+)\)",
            str(text),
            flags=re.IGNORECASE,
        )

        if center_match is not None:

            center = _parse_coordinate_values(
                center_match.group(1)
            )

            if (
                center is not None
                and len(center) >= 2
            ):
                arguments["center_x"] = (
                    center[0]
                )
                arguments["center_y"] = (
                    center[1]
                )

    return arguments



def _parse_general_scalar(value):
    """
    Parse a simple scalar token used by semantic adapters.

    Numeric strings become int/float. Symbolic values such as pi,
    pi/2, 2*pi, or simple expressions remain strings so the
    deterministic subsystem can parse them with SymPy.
    """

    value = _clean_extracted_text(value)

    if value is None:
        return None

    if re.fullmatch(NUMBER_PATTERN, value):

        number = float(value)

        if number.is_integer():
            return int(number)

        return number

    return value


def _extract_from_to_pair(text):
    """
    Extract a generic 'from X to Y' pair.

    Examples:
        from 0 to 5
        from 1 to 10
        from 0 to 2*pi
    """

    match = re.search(
        r"\bfrom\s+(.+?)\s+to\s+(.+?)"
        r"(?=\s+(?:using|with|where|for)\b|[,;]|$)",
        str(text),
        flags=re.IGNORECASE,
    )

    if match is None:
        return None

    first = _parse_general_scalar(
        match.group(1)
    )

    second = _parse_general_scalar(
        match.group(2)
    )

    if first is None or second is None:
        return None

    return first, second


def _extract_expression_before_bounds(text):
    """
    Extract the mathematical expression preceding 'from X to Y'
    for common calculus/series requests.
    """

    patterns = [
        r"\bof\s+(.+?)\s+from\s+.+?\s+to\s+.+?(?:$|[,;])",
        r"\bsum\s+of\s+(.+?)\s+from\s+.+?\s+to\s+.+?(?:$|[,;])",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            str(text),
            flags=re.IGNORECASE,
        )

        if match is not None:

            value = _clean_extracted_text(
                match.group(1)
            )

            if value is not None:
                return value

    return None


def _extract_named_symbolic_value(
    text,
    alias,
):
    """
    Extract a named scalar that may be numeric or symbolic.

    Unlike extract_named_number(), this supports values such as:
        angle pi/2
        angle 2*pi
    """

    pattern = (
        rf"\b{re.escape(alias)}\b"
        rf"\s*(?:of|is|equals|=|:)?\s*"
        rf"([+\-]?(?:\d+(?:\.\d+)?|"
        rf"(?:\d+\s*\*\s*)?pi(?:\s*/\s*\d+)?))"
    )

    match = re.search(
        pattern,
        str(text),
        flags=re.IGNORECASE,
    )

    if match is None:
        return None

    return _parse_general_scalar(
        match.group(1)
    )


def _extract_named_expression_pair(
    text,
    first_name,
    second_name,
):
    """
    Extract two explicitly named symbolic expressions while
    stopping the first expression before the second parameter.

    Examples:
        first x**2 and second sin(x)
        numerator x**2 and denominator x + 1
        u x and dv exp(x)
        upper function x**2 and lower function x
    """

    first_aliases = sorted(
        get_parameter_aliases(first_name),
        key=len,
        reverse=True,
    )

    second_aliases = sorted(
        get_parameter_aliases(second_name),
        key=len,
        reverse=True,
    )

    first_alias_pattern = "|".join(
        re.escape(alias)
        for alias in first_aliases
    )

    second_alias_pattern = "|".join(
        re.escape(alias)
        for alias in second_aliases
    )

    pattern = (
        rf"\b(?:{first_alias_pattern})\b"
        rf"\s*(?:is|=|:)?\s*"
        rf"(.+?)"
        rf"\s+(?:and\s+)?"
        rf"\b(?:{second_alias_pattern})\b"
        rf"\s*(?:is|=|:)?\s*"
        rf"(.+?)"
        rf"(?=\s+from\b|\s+between\b|[,;]|$)"
    )

    match = re.search(
        pattern,
        str(text),
        flags=re.IGNORECASE,
    )

    if match is None:
        return {}

    first = _clean_extracted_text(
        match.group(1)
    )

    second = _clean_extracted_text(
        match.group(2)
    )

    result = {}

    if first is not None:
        result[first_name] = first

    if second is not None:
        result[second_name] = second

    return result



def _extract_direct_trig_arguments(
    text,
    operation_name,
    parameter_names,
):
    """
    Extract arguments from direct trigonometric function-call syntax.

    Examples:
        sin(pi/6)     -> {"angle": "pi/6"}
        cos(pi/3)     -> {"angle": "pi/3"}
        tan(45)       -> {"angle": 45}
        asin(1/2)     -> {"value": "1/2"}

    This adapter only applies to the nine basic direct trig operations.
    It does not handle trig equations or identity/transform operations.
    """

    operation_aliases = {
        "sine": ("sine", "sin"),
        "cosine": ("cosine", "cos"),
        "tangent": ("tangent", "tan"),
        "secant": ("secant", "sec"),
        "cosecant": ("cosecant", "csc"),
        "cotangent": ("cotangent", "cot"),
        "arcsine": ("arcsine", "asin", "arcsin"),
        "arccosine": ("arccosine", "acos", "arccos"),
        "arctangent": ("arctangent", "atan", "arctan"),
    }

    aliases = operation_aliases.get(
        operation_name
    )

    if aliases is None:
        return {}

    parameter_set = set(
        parameter_names
    )

    target_parameter = (
        "value"
        if operation_name in {
            "arcsine",
            "arccosine",
            "arctangent",
        }
        else "angle"
    )

    if target_parameter not in parameter_set:
        return {}

    alias_pattern = "|".join(
        re.escape(alias)
        for alias in sorted(
            aliases,
            key=len,
            reverse=True,
        )
    )

    match = re.search(
        rf"\b(?:{alias_pattern})\s*\(\s*([^()]+?)\s*\)",
        str(text),
        flags=re.IGNORECASE,
    )

    # Also support natural-language direct trig requests:
    #
    #     sine of pi/6
    #     cosine of pi/3
    #     tangent of 45
    #     arcsine of 1/2
    #
    # Keep the accepted value deliberately narrow so this adapter
    # does not steal full trig equations or larger expressions.

    if match is None:

        scalar_pattern = (
            r"[+\-]?(?:"
            r"\d+(?:\.\d+)?(?:\s*/\s*\d+(?:\.\d+)?)?"
            r"|(?:\d+(?:\.\d+)?\s*\*\s*)?"
            r"pi(?:\s*/\s*\d+(?:\.\d+)?)?"
            r")"
        )

        match = re.search(
            rf"\b(?:{alias_pattern})\b\s+(?:of\s+)?"
            rf"({scalar_pattern})",
            str(text),
            flags=re.IGNORECASE,
        )

    if match is None:
        return {}

    value = _parse_general_scalar(
        match.group(1)
    )

    if value is None:
        return {}

    return {
        target_parameter: value
    }

def extract_semantic_arguments_for_operation(
    text,
    operation_name,
    parameter_names,
):
    """
    Reusable operation-aware semantic adapters.

    These adapters cover language patterns that cannot be recovered
    reliably from a parameter name alone. They are intentionally
    grouped by signature pattern rather than creating hundreds of
    one-off parsers.
    """

    text = str(text)
    parameter_names = list(parameter_names)
    parameter_set = set(parameter_names)
    result = {}

    # --------------------------------------------------------
    # DIRECT TRIGONOMETRIC FUNCTION CALLS
    # --------------------------------------------------------

    direct_trig_arguments = (
        _extract_direct_trig_arguments(
            text,
            operation_name,
            parameter_names,
        )
    )

    result.update(
        direct_trig_arguments
    )

    # --------------------------------------------------------
    # BASIC TWO-OPERAND ARITHMETIC
    # --------------------------------------------------------

    if {"a", "b"}.issubset(parameter_set):

        patterns = []

        # Support both natural-language arithmetic and direct
        # operator notation.  The direct forms intentionally
        # stay limited to two plain numeric operands so this
        # adapter does not steal symbolic algebra expressions.

        if operation_name == "add":
            patterns = [
                rf"({NUMBER_PATTERN})\s*\+\s*({NUMBER_PATTERN})",
                rf"\badd\s+({NUMBER_PATTERN})\s+(?:and|to)\s+"
                rf"({NUMBER_PATTERN})\b",
            ]

        elif operation_name == "multiply":
            patterns = [
                rf"({NUMBER_PATTERN})\s*(?:\*|×)\s*({NUMBER_PATTERN})",
                rf"\bmultiply\s+({NUMBER_PATTERN})\s+(?:and|by)\s+"
                rf"({NUMBER_PATTERN})\b",
            ]

        elif operation_name in {
            "greatest_common_divisor",
            "least_common_multiple",
            "ratio",
        }:
            patterns = [
                rf"\b(?:gcd|lcm|ratio(?:\s+of)?)\s+"
                rf"({NUMBER_PATTERN})\s+(?:and|by|to)\s+"
                rf"({NUMBER_PATTERN})\b",
            ]

        elif operation_name == "subtract":
            patterns = [
                rf"({NUMBER_PATTERN})\s*-\s*({NUMBER_PATTERN})",
                rf"\bsubtract\s+({NUMBER_PATTERN})\s+from\s+"
                rf"({NUMBER_PATTERN})\b",
            ]

        elif operation_name == "divide":
            patterns = [
                rf"({NUMBER_PATTERN})\s*(?:/|÷)\s*({NUMBER_PATTERN})",
                rf"\bdivide\s+({NUMBER_PATTERN})\s+by\s+"
                rf"({NUMBER_PATTERN})\b",
            ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            )

            if match is not None:

                first = _parse_general_scalar(
                    match.group(1)
                )

                second = _parse_general_scalar(
                    match.group(2)
                )

                if (
                    operation_name == "subtract"
                    and re.search(
                        r"\bsubtract\b",
                        match.group(0),
                        flags=re.IGNORECASE,
                    )
                ):
                    # "subtract 4 from 10" => 10 - 4
                    result["a"] = second
                    result["b"] = first
                else:
                    # Direct notation such as "10 - 4" keeps
                    # the operands in their written order.
                    result["a"] = first
                    result["b"] = second

                break

    # --------------------------------------------------------
    # POWER LANGUAGE
    # --------------------------------------------------------

    if {"base", "exponent"}.issubset(
        parameter_set
    ):

        match = re.search(
            rf"\braise\s+({NUMBER_PATTERN})\s+"
            rf"to\s+(?:the\s+)?power\s+({NUMBER_PATTERN})\b",
            text,
            flags=re.IGNORECASE,
        )

        if match is not None:
            result["base"] = _parse_general_scalar(
                match.group(1)
            )
            result["exponent"] = _parse_general_scalar(
                match.group(2)
            )

    # --------------------------------------------------------
    # SYMBOLIC EXPRESSION PAIRS
    # --------------------------------------------------------

    expression_pairs = [
        ("first", "second"),
        ("numerator", "denominator"),
        ("u", "dv"),
        ("upper_function", "lower_function"),
        ("dividend", "divisor"),
    ]

    for first_name, second_name in expression_pairs:

        if {
            first_name,
            second_name,
        }.issubset(parameter_set):

            result.update(
                _extract_named_expression_pair(
                    text,
                    first_name,
                    second_name,
                )
            )

    # --------------------------------------------------------
    # COMMON FROM/TO BOUNDS
    # --------------------------------------------------------

    bound_pair = _extract_from_to_pair(
        text
    )

    if bound_pair is not None:

        first_bound, second_bound = (
            bound_pair
        )

        if {
            "lower",
            "upper",
        }.issubset(parameter_set):
            result["lower"] = first_bound
            result["upper"] = second_bound

        if {
            "start",
            "end",
        }.issubset(parameter_set):
            result["start"] = first_bound
            result["end"] = second_bound

    # --------------------------------------------------------
    # EXPRESSION BEFORE FROM/TO BOUNDS
    # --------------------------------------------------------

    if (
        "expression" in parameter_set
        and "expression" not in result
    ):

        bounded_expression = (
            _extract_expression_before_bounds(
                text
            )
        )

        if bounded_expression is not None:
            result["expression"] = (
                bounded_expression
            )

    # --------------------------------------------------------
    # RIEMANN / NUMERICAL RECTANGLE COUNT
    # --------------------------------------------------------

    if "rectangles" in parameter_set:

        match = re.search(
            rf"\b(?:using|with)\s+({NUMBER_PATTERN})\s+"
            rf"rectangles?\b",
            text,
            flags=re.IGNORECASE,
        )

        if match is not None:
            result["rectangles"] = int(
                float(match.group(1))
            )

    # --------------------------------------------------------
    # SYMBOLIC ANGLES
    # --------------------------------------------------------

    if "angle" in parameter_set:

        angle = _extract_named_symbolic_value(
            text,
            "angle",
        )

        if angle is not None:
            result["angle"] = angle

    return result


def extract_argument(
    text,
    parameter_name,
    operation_name=None,
):
    """
    Extract one argument according to SATURN's language schema.

    Supported Interpreter v2 argument types currently include:

        number
        integer
        angle
        expression
        variable
    """

    parameter_type = get_parameter_type(
        parameter_name,
        operation_name=operation_name,
    )

    # --------------------------------------------------------
    # NUMERIC VALUES
    # --------------------------------------------------------

    if parameter_type in {
        "number",
        "integer",
        "angle",
    }:

        value = extract_named_number(
            text,
            parameter_name,
        )

        if (
            value is not None
            and parameter_type == "integer"
        ):
            return int(value)

        return value

    # --------------------------------------------------------
    # SYMBOLIC EXPRESSIONS
    # --------------------------------------------------------

    if parameter_type == "expression":

        return extract_expression(
            text,
            parameter_name,
        )

    # --------------------------------------------------------
    # EQUATIONS / INEQUALITIES
    # --------------------------------------------------------

    if parameter_type == "equation":

        return extract_equation(
            text,
            parameter_name,
        )

    # --------------------------------------------------------
    # EQUATION LISTS
    # --------------------------------------------------------

    if parameter_type == "equation_list":

        return extract_equation_list(
            text,
            parameter_name,
        )

    # --------------------------------------------------------
    # VARIABLES
    # --------------------------------------------------------

    if parameter_type == "variable":

        return extract_variable(
            text,
            parameter_name,
        )

    # --------------------------------------------------------
    # VARIABLE LISTS
    # --------------------------------------------------------

    if parameter_type == "variable_list":

        return extract_variable_list(
            text,
            parameter_name,
        )
    
        # --------------------------------------------------------
    # POINTS
    # --------------------------------------------------------

    if parameter_type == "point":

        return extract_point(
            text,
            parameter_name,
        )

    # --------------------------------------------------------
    # VECTORS
    # --------------------------------------------------------

    if parameter_type == "vector":

        return extract_vector(
            text,
            parameter_name,
        )

    # --------------------------------------------------------
    # GENERIC LISTS / COMPONENTS
    # --------------------------------------------------------

    if parameter_type == "list":

        return extract_list(
            text,
            parameter_name,
        )

    # --------------------------------------------------------
    # MAPPINGS / SUBSTITUTIONS
    # --------------------------------------------------------

    if parameter_type == "mapping":

        return extract_mapping(
            text,
            parameter_name,
        )

    # --------------------------------------------------------
    # STRINGS / ENUM-LIKE OPTIONS
    # --------------------------------------------------------

    if parameter_type == "string":

        return extract_string(
            text,
            parameter_name,
        )

    # --------------------------------------------------------
    # BOOLEAN OPTIONS
    # --------------------------------------------------------

    if parameter_type == "boolean":

        return extract_boolean(
            text,
            parameter_name,
        )

    # --------------------------------------------------------
    # BOUNDS / INTERVALS
    # --------------------------------------------------------

    if parameter_type == "bounds":

        return extract_bounds(
            text,
            parameter_name,
        )

    return None


def extract_arguments(text, parameter_names):
    """
    Extract all supported arguments requested by a selected
    deterministic math operation.

    Returns both extracted and missing arguments.
    """

    arguments = {}
    missing = []

    for parameter_name in parameter_names:

        value = extract_argument(
            text,
            parameter_name,
        )

        if value is None:
            missing.append(
                parameter_name
            )
        else:
            arguments[
                parameter_name
            ] = value

    return {
        "arguments": arguments,
        "missing": missing,
    }

def get_operation_parameters(operation_name):
    """
    Inspect a registered deterministic math operation and
    return information about its Python parameters.
    """

    operation = math_registry.get(
        operation_name
    )

    if operation is None:
        return {
            "success": False,
            "operation": operation_name,
            "parameters": [],
            "required": [],
            "optional": [],
            "error": (
                f"Unknown math operation: "
                f"'{operation_name}'"
            ),
        }

    function = operation["function"]

    signature = inspect.signature(
        function
    )

    parameters = []
    required = []
    optional = []

    for parameter_name, parameter in (
        signature.parameters.items()
    ):

        if parameter.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            continue

        is_required = (
            parameter.default
            is inspect.Parameter.empty
        )

        parameter_info = {
            "name": parameter_name,
            "type": get_parameter_type(
                parameter_name,
                operation_name=operation_name,
            ),
            "required": is_required,
            "default": (
                None
                if is_required
                else parameter.default
            ),
        }

        parameters.append(
            parameter_info
        )

        if is_required:
            required.append(
                parameter_name
            )
        else:
            optional.append(
                parameter_name
            )

    return {
        "success": True,
        "operation": operation_name,
        "parameters": parameters,
        "required": required,
        "optional": optional,
        "error": None,
    }


def extract_arguments_for_operation(
    text,
    operation_name,
):
    """
    Extract natural-language arguments for a registered
    deterministic math operation.

    SATURN uses the operation's real Python signature to
    determine what parameters should be searched for.
    """

    operation_parameters = (
        get_operation_parameters(
            operation_name
        )
    )

    result = {
        "success": False,
        "operation": operation_name,
        "arguments": {},
        "missing_required": [],
        "unparsed_required": [],
        "optional_found": [],
        "parameters": [],
        "error": None,
    }

    if not operation_parameters["success"]:

        result["error"] = (
            operation_parameters["error"]
        )

        return result

    result["parameters"] = (
        operation_parameters[
            "parameters"
        ]
    )

    # --------------------------------------------------------
    # SIGNATURE-DRIVEN COORDINATE ADAPTERS
    # --------------------------------------------------------

    all_parameter_names = [
        parameter["name"]
        for parameter in operation_parameters[
            "parameters"
        ]
    ]

    coordinate_arguments = (
        extract_coordinate_arguments(
            text,
            all_parameter_names,
        )
    )

    result["arguments"].update(
        coordinate_arguments
    )

    # --------------------------------------------------------
    # REUSABLE OPERATION-AWARE SEMANTIC ADAPTERS
    # --------------------------------------------------------

    semantic_arguments = (
        extract_semantic_arguments_for_operation(
            text,
            operation_name,
            all_parameter_names,
        )
    )

    result["arguments"].update(
        semantic_arguments
    )

    # --------------------------------------------------------
    # REQUIRED PARAMETERS
    # --------------------------------------------------------

    for parameter_name in (
        operation_parameters["required"]
    ):

        if parameter_name in result["arguments"]:
            continue

        parameter_type = get_parameter_type(
            parameter_name,
            operation_name=operation_name,
        )

        value = extract_argument(
            text,
            parameter_name,
            operation_name=operation_name,
        )

        if value is not None:

            result["arguments"][
                parameter_name
            ] = value

        else:

            # Known language type, but value was not present.
            if parameter_type != "unknown":

                result["missing_required"].append(
                    parameter_name
                )

            # SATURN does not yet know how to interpret this
            # parameter type.
            else:

                result["unparsed_required"].append(
                    parameter_name
                )

    # --------------------------------------------------------
    # OPTIONAL PARAMETERS
    # --------------------------------------------------------

    for parameter_name in (
        operation_parameters["optional"]
    ):

        if parameter_name in result["arguments"]:
            result["optional_found"].append(
                parameter_name
            )
            continue

        value = extract_argument(
            text,
            parameter_name,
            operation_name=operation_name,
        )

        if value is not None:

            result["arguments"][
                parameter_name
            ] = value

            result["optional_found"].append(
                parameter_name
            )

    result["success"] = (
        len(
            result["missing_required"]
        ) == 0
        and len(
            result["unparsed_required"]
        ) == 0
    )

    return result