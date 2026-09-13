import re


# ============================================================
# LANGUAGE NORMALIZATION
# ============================================================

PHRASE_REPLACEMENTS = {
    "differentiate": "derivative",
    "differentiation": "derivative",
    "take the derivative": "derivative",
    "find the derivative": "derivative",

    "integrate": "integral",
    "integration": "integral",
    "find the integral": "integral",

    "plus": "+",
    "minus": "-",
    "times": "*",
    "multiplied by": "*",
    "divided by": "/",

    "squared": "**2",
    "cubed": "**3",
}


def normalize_math_language(text):
    """
    Normalize common mathematical language into forms that
    are easier for SATURN's deterministic systems to process.

    This function does not perform any mathematics.
    """

    text = str(text).strip().lower()

    # Longer phrases should be replaced first.
    replacements = sorted(
        PHRASE_REPLACEMENTS.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for phrase, replacement in replacements:
        text = text.replace(
            phrase,
            replacement
        )

    # --------------------------------------------------------
    # NATURAL-LANGUAGE FRACTIONS
    # --------------------------------------------------------
    #
    # Keep "over" contextual rather than replacing every use of
    # the word globally. This protects unrelated mathematical
    # phrases while supporting common spoken forms such as:
    #
    #     pi over 6       -> pi/6
    #     2 pi over 3     -> 2*pi/3
    #     1 over 2        -> 1/2
    # --------------------------------------------------------

    text = re.sub(
        r"\b(-?\d+(?:\.\d+)?)\s+pi\s+over\s+"
        r"(-?\d+(?:\.\d+)?)\b",
        r"\1*pi/\2",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\bpi\s+over\s+(-?\d+(?:\.\d+)?)\b",
        r"pi/\1",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\b(-?\d+(?:\.\d+)?)\s+over\s+"
        r"(-?\d+(?:\.\d+)?)\b",
        r"\1/\2",
        text,
        flags=re.IGNORECASE,
    )

    # --------------------------------------------------------
    # IMPLICIT MULTIPLICATION
    # --------------------------------------------------------
    #
    # Convert simple coefficient-variable notation into explicit
    # multiplication so SymPy and SATURN's extractors receive:
    #
    #     3x   -> 3*x
    #     12y  -> 12*y
    #
    # This is intentionally conservative in this cleanup pass.
    # --------------------------------------------------------

    text = re.sub(
        r"(?<![A-Za-z0-9_])(\d+(?:\.\d+)?)\s*([A-Za-z])\b",
        r"\1*\2",
        text,
    )

    # Normalize repeated whitespace.
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# ============================================================
# SYMBOLIC ALGEBRA DETECTION
# ============================================================

def _contains_symbolic_algebra_structure(text):
    """
    Return True when text contains a variable participating in
    recognizable algebraic expression syntax.

    Examples:
        x**2 + 3*x + 2
        y^3
        4*x - 7 = 21

    This prevents numeric fragments inside symbolic expressions
    from being mistaken for standalone arithmetic.
    """

    text = str(text)

    patterns = [
        r"\b[A-Za-z]\b\s*(?:\*\*|\^|[+\-*/=])",
        r"(?:\*\*|\^|[+\-*/=])\s*\b[A-Za-z]\b",
        r"\b\d+(?:\.\d+)?\s*\*\s*[A-Za-z]\b",
    ]

    return any(
        re.search(pattern, text)
        for pattern in patterns
    )


def extract_bare_symbolic_expression(text):
    """
    Extract a symbolic expression when the user supplied an
    expression but did not request a mathematical operation.

    Examples:
        "what is x**2 + 3*x + 2?" -> "x**2 + 3*x + 2"
        "what is x**3?"           -> "x**3"

    Explicit operation requests such as factor, simplify, solve,
    derivative, and integral are intentionally excluded.
    """

    text = str(text).strip()

    operation_cues = (
        "solve",
        "factor",
        "expand",
        "simplify",
        "derivative",
        "integral",
        "differentiate",
        "integrate",
        "evaluate",
        "calculate",
        "compute",
        "find roots",
        "roots of",
    )

    lowered = text.lower()

    if any(
        cue in lowered
        for cue in operation_cues
    ):
        return None

    cleaned = re.sub(
        r"^\s*(?:what\s+is|what's)\s+",
        "",
        text,
        flags=re.IGNORECASE,
    )

    cleaned = cleaned.strip(" .?!")

    if not cleaned:
        return None

    # Require symbolic structure rather than a plain word or number.
    if not _contains_symbolic_algebra_structure(cleaned):
        return None

    # Keep this path conservative: only expression characters.
    if not re.fullmatch(
        r"[0-9A-Za-z_+\-*/^().\s]+",
        cleaned,
    ):
        return None

    return cleaned


# ============================================================
# SUBSYSTEM DETECTION
# ============================================================

SUBSYSTEM_KEYWORDS = {
    "arithmetic": {
        "add",
        "subtract",
        "multiply",
        "divide",
        "percentage",
        "percent",
        "factorial",
        "gcd",
        "lcm",
    },

    "algebra": {
        "equation",
        "solve",
        "factor",
        "expand",
        "simplify",
        "polynomial",
        "quadratic",
        "inequality",
        "roots",
    },

    "geometry": {
        "circle",
        "triangle",
        "rectangle",
        "square",
        "sphere",
        "cube",
        "cylinder",
        "cone",
        "polygon",
        "area",
        "perimeter",
        "circumference",
        "volume",
        "radius",
        "diameter",
    },

    "trigonometry": {
        "sine",
        "cosine",
        "tangent",
        "sin",
        "cos",
        "tan",
        "arcsine",
        "arccosine",
        "arctangent",
        "arcsin",
        "arccos",
        "arctan",
        "angle",
        "trigonometry",
        "trig",
        "bearing",
    },

    "calculus": {
        "derivative",
        "integral",
        "limit",
        "continuity",
        "gradient",
        "partial",
        "taylor",
        "maclaurin",
        "divergence",
        "curl",
    },
}


def detect_subsystem(text):
    """
    Estimate the most likely math subsystem from language.

    Returns:
        subsystem name or None
    """

    text = str(text)

    # --------------------------------------------------------
    # EXPLICIT TRIGONOMETRY INTENT
    # --------------------------------------------------------
    #
    # Normalization can turn:
    #
    #     "arcsine of 1 over 2"
    #
    # into:
    #
    #     "arcsine of 1/2"
    #
    # The slash is arithmetic notation, but the requested operation
    # is still trigonometric. Explicit trig language therefore takes
    # precedence over direct arithmetic-symbol detection.
    # --------------------------------------------------------

    trig_intent_pattern = (
        r"\b(?:"
        r"sine|cosine|tangent|secant|cosecant|cotangent|"
        r"sin|cos|tan|sec|csc|cot|"
        r"arcsine|arccosine|arctangent|"
        r"arcsin|arccos|arctan|"
        r"trigonometry|trig"
        r")\b"
    )

    if re.search(
        trig_intent_pattern,
        text,
        flags=re.IGNORECASE,
    ):
        return "trigonometry"

    # --------------------------------------------------------
    # EXPLICIT CALCULUS INTENT
    # --------------------------------------------------------

    if re.search(
        r"\b(?:derivative|integral|limit|continuity|gradient|"
        r"partial|taylor|maclaurin|divergence|curl)\b",
        text,
        flags=re.IGNORECASE,
    ):
        return "calculus"

    # --------------------------------------------------------
    # EXPLICIT ALGEBRA INTENT
    # --------------------------------------------------------

    if re.search(
        r"\b(?:equation|solve|factor|expand|simplify|polynomial|"
        r"quadratic|inequality|root|roots)\b",
        text,
        flags=re.IGNORECASE,
    ):
        return "algebra"

    # --------------------------------------------------------
    # SYMBOLIC ALGEBRA STRUCTURE
    # --------------------------------------------------------
    #
    # This must occur before direct arithmetic detection. Otherwise
    # text such as "x**2 + 3*x + 2" can accidentally expose the
    # numeric fragment "2 + 3" and be routed as addition.
    # --------------------------------------------------------

    if _contains_symbolic_algebra_structure(
        text
    ):
        return "algebra"

    # --------------------------------------------------------
    # DIRECT ARITHMETIC SYMBOLS
    # --------------------------------------------------------
    #
    # Recognize simple binary arithmetic before word-based
    # subsystem scoring.
    #
    # Examples:
    #     17 + 28
    #     10 - 4
    #     6 * 7
    #     20 / 5
    # --------------------------------------------------------

    number_pattern = r"-?\d+(?:\.\d+)?"

    direct_arithmetic_patterns = [
        rf"{number_pattern}\s*\+\s*{number_pattern}",
        rf"{number_pattern}\s*-\s*{number_pattern}",
        rf"{number_pattern}\s*\*\s*{number_pattern}",
        rf"{number_pattern}\s*/\s*{number_pattern}",
    ]

    if any(
        re.search(pattern, text)
        for pattern in direct_arithmetic_patterns
    ):
        return "arithmetic"

    words = set(
        re.findall(
            r"[a-zA-Z]+",
            text.lower()
        )
    )

    scores = {}

    for subsystem, keywords in SUBSYSTEM_KEYWORDS.items():
        scores[subsystem] = len(
            words & keywords
        )

    highest_score = max(
        scores.values(),
        default=0
    )

    if highest_score == 0:
        return None

    winners = [
        subsystem
        for subsystem, score in scores.items()
        if score == highest_score
    ]

    # Do not guess when subsystem evidence is tied.
    if len(winners) != 1:
        return None

    return winners[0]


# ============================================================
# VARIABLE EXTRACTION
# ============================================================

def extract_variable(text):
    """
    Extract an explicitly stated differentiation/integration
    variable when possible.

    Examples:
        "with respect to x"
        "in terms of t"
    """

    patterns = [
        r"with respect to\s+([a-zA-Z])",
        r"in terms of\s+([a-zA-Z])",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1)

    return None


# ============================================================
# RADIUS EXTRACTION
# ============================================================

def extract_radius(text):
    """
    Extract a simple numeric radius from natural language.

    Examples:
        "radius 7"
        "radius of 7"
        "radius is 7"
        "radius = 7"
    """

    pattern = (
        r"\bradius"
        r"(?:\s+of|\s+is|\s*=)?"
        r"\s*(-?\d+(?:\.\d+)?)"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if not match:
        return None

    value = match.group(1)

    if "." in value:
        return float(value)

    return int(value)


# ============================================================
# EXPRESSION EXTRACTION
# ============================================================

def extract_calculus_expression(text):
    """
    Attempt to extract a simple expression from a calculus
    request.

    This is intentionally conservative in Interpreter v1.
    """

    cleaned = text

    # Remove common operation language.
    cleaned = re.sub(
        r"\b(?:find|calculate|compute|evaluate)\b",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    cleaned = re.sub(
        r"\b(?:the\s+)?(?:derivative|integral)\s+of\b",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    cleaned = re.sub(
        r"\b(?:the\s+)?(?:derivative|integral)\b",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    # Remove variable phrases.
    cleaned = re.sub(
        r"\bwith respect to\s+[a-zA-Z]\b",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    cleaned = re.sub(
        r"\bin terms of\s+[a-zA-Z]\b",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    # Remove punctuation that commonly ends a sentence.
    cleaned = cleaned.strip(
        " .?!"
    )

    # Normalize multiplication such as:
    # 2x -> 2*x
    cleaned = re.sub(
        r"(\d)([a-zA-Z])",
        r"\1*\2",
        cleaned
    )

    cleaned = re.sub(
        r"\s+",
        " ",
        cleaned
    ).strip()

    if not cleaned:
        return None

    # Only return something that appears to contain
    # mathematical content.
    if not re.search(
        r"[0-9a-zA-Z+\-*/^()]",
        cleaned
    ):
        return None

    return cleaned


# ============================================================
# ARGUMENT EXTRACTION
# ============================================================

def extract_arguments(
    original_text,
    normalized_text,
    subsystem
):
    """
    Extract simple operation arguments from a request.

    Interpreter v1 only supports a limited set of patterns.
    More sophisticated parsing will be added later.
    """

    arguments = {}

    # --------------------------------------------------------
    # GEOMETRY
    # --------------------------------------------------------

    if subsystem == "geometry":

        radius = extract_radius(
            normalized_text
        )

        if radius is not None:
            arguments["radius"] = radius

    # --------------------------------------------------------
    # CALCULUS
    # --------------------------------------------------------

    if subsystem == "calculus":

        variable = extract_variable(
            normalized_text
        )

        expression = extract_calculus_expression(
            normalized_text
        )

        if expression is not None:
            arguments[
                "expression"
            ] = expression

        if variable is not None:
            arguments[
                "variable"
            ] = variable

    return arguments


# ============================================================
# ROUTER QUERY GENERATION
# ============================================================

def build_router_query(
    normalized_text,
    subsystem
):
    """
    Build a simplified query for the math router.

    Interpreter v1 intentionally preserves most of the
    original wording because the router already knows how
    to rank registry metadata.
    """

    query = normalized_text

    # Remove simple numeric values.
    query = re.sub(
        r"-?\d+(?:\.\d+)?",
        " ",
        query
    )

    # Remove obvious equation/expression syntax from the
    # routing query while preserving operation words.
    query = re.sub(
        r"\*\*\d+",
        " ",
        query
    )

    query = re.sub(
        r"[=+*/()]",
        " ",
        query
    )

    query = re.sub(
        r"\s+",
        " ",
        query
    ).strip()

    return query


# ============================================================
# MAIN INTERPRETER
# ============================================================

def interpret_math_request(text):
    """
    Convert a natural-language math request into a
    structured SATURN math request.

    The interpreter does not perform mathematics and does
    not directly select or execute a registry operation.

    Returns:
        {
            "success": bool,
            "original_text": str,
            "normalized_text": str,
            "query": str,
            "subsystem": str or None,
            "arguments": dict,
            "warnings": list,
            "error": str or None
        }
    """

    original_text = str(text).strip()

    result = {
        "success": False,
        "original_text": original_text,
        "normalized_text": "",
        "query": "",
        "subsystem": None,
        "arguments": {},
        "bare_expression": None,
        "warnings": [],
        "error": None
    }

    # --------------------------------------------------------
    # EMPTY REQUEST
    # --------------------------------------------------------

    if not original_text:
        result["error"] = (
            "No math request was provided."
        )

        return result

    # --------------------------------------------------------
    # NORMALIZE LANGUAGE
    # --------------------------------------------------------

    normalized_text = normalize_math_language(
        original_text
    )

    result[
        "normalized_text"
    ] = normalized_text

    # --------------------------------------------------------
    # DETECT SUBSYSTEM
    # --------------------------------------------------------

    subsystem = detect_subsystem(
        normalized_text
    )

    result[
        "subsystem"
    ] = subsystem

    if subsystem is None:
        result["warnings"].append(
            "The math subsystem could not be "
            "determined confidently."
        )

    # --------------------------------------------------------
    # EXTRACT ARGUMENTS
    # --------------------------------------------------------

    arguments = extract_arguments(
        original_text=original_text,
        normalized_text=normalized_text,
        subsystem=subsystem
    )

    result[
        "arguments"
    ] = arguments

    # --------------------------------------------------------
    # BARE SYMBOLIC EXPRESSION
    # --------------------------------------------------------
    #
    # If the user supplied a valid symbolic expression without
    # requesting an operation, preserve that intent rather than
    # inventing simplify/factor/solve behavior.
    # --------------------------------------------------------

    if subsystem == "algebra":
        result[
            "bare_expression"
        ] = extract_bare_symbolic_expression(
            normalized_text
        )

    # --------------------------------------------------------
    # BUILD ROUTER QUERY
    # --------------------------------------------------------

    router_query = build_router_query(
        normalized_text,
        subsystem
    )

    result[
        "query"
    ] = router_query

    # --------------------------------------------------------
    # INTERPRETATION COMPLETE
    # --------------------------------------------------------

    result[
        "success"
    ] = True

    return result