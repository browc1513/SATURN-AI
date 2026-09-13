# ============================================================
# S.A.T.U.R.N. LANGUAGE SCHEMA
# ============================================================

# This file defines how SATURN should interpret parameter names
# found in registered deterministic math operations.
#
# It does NOT perform calculations.
# It helps translate natural language into structured arguments.


# ============================================================
# PARAMETER TYPE GROUPS
# ============================================================

NUMERIC_PARAMETERS = {
    "value",
    "number",
    "amount",

    "radius",
    "radius_1",
    "radius_2",
    "radius_squared",
    "inner_radius",
    "outer_radius",
    "distance_from_center",
    "chord",

    "diameter",
    "length",
    "width",
    "height",
    "base",
    "base_1",
    "base_2",
    "base_area",
    "base_perimeter",
    "base_side",
    "side",
    "side_a",
    "side_b",
    "side_c",
    "side_d",
    "second_side",
    "known_side",
    "target_side",
    "included_side",
    "equal_side",
    "known_leg",
    "hypotenuse",
    "opposite",
    "adjacent",
    "opposite_side",
    "adjacent_side_1",
    "adjacent_side_2",

    "diagonal_1",
    "diagonal_2",
    "slant_height",
    "prism_length",

    "area",
    "volume",
    "circumference",
    "perimeter",
    "distance",

    "slope",
    "slope_1",
    "slope_2",
    "slope_value",
    "line_slope",
    "y_intercept",
    "intercept_1",
    "intercept_2",

    "x",
    "y",
    "z",
    "x1",
    "y1",
    "x2",
    "y2",
    "x3",
    "y3",
    "center_x",
    "center_y",

    "x_component",
    "y_component",
    "magnitude",

    "horizontal_distance",
    "vertical_height",
    "vertical_drop",

    "original",
    "new",
    "original_length",
    "new_length",
    "original_area",
    "original_volume",
    "scale_factor",
    "scale_factor_value",

    "exact_value",
    "approximate_value",

    "first_term",
    "index_value",
    "level",

    "part",
    "whole",

    "delta_x",
    "delta_y",

    "parameter_value",
    "a",
    "b",
    "c",
    "d",
    "h",
    "k",
    "ratio",
    "exponent",
    "side_length",
    "apothem",
    "triangle_base",
    "triangle_height",

}


INTEGER_PARAMETERS = {
    "order",
    "degree",
    "n",
    "digits",
    "significant_digits",
    "number_of_sides",
    "rotations",
    "quadrant",
    "intervals",
    "index",
    "rectangles",

}


ANGLE_PARAMETERS = {
    "angle",
    "angle_a",
    "angle_b",
    "angle_c",
    "theta",
    "phi",
    "degrees",
    "radians",
    "bearing",
    "direction_angle",
    "angle_1",
    "angle_2",
    "angle_3",
    "angle_degrees",
    "central_angle_degrees",
    "included_angle",
    "known_angle",
    "target_angle",
    "lower_angle",
    "upper_angle",
    "remote_angle_1",
    "remote_angle_2",

}


EXPRESSION_PARAMETERS = {
    "expression",
    "left_side",
    "right_side",
    "expression_1",
    "expression_2",
    "inner_expression",
    "outer_expression",
    "radius_expression",
    "radius_function",
    "x_expression",
    "y_expression",
    "scalar_field",
    "potential_function",
    "objective",
    "constraint",
    "candidate",
    "candidate_derivative",
    "original",
    "upper_function",
    "lower_function",
    "integrand",
    "u",
    "dv",
    "first",
    "second",
    "dividend",
    "divisor",
    "numerator",
    "denominator",

}


EQUATION_PARAMETERS = {
    "equation",
    "inequality",
}


EQUATION_LIST_PARAMETERS = {
    "equations",
}


VARIABLE_PARAMETERS = {
    "variable",
    "dependent",
    "independent",
    "outer_variable",
    "output_variable",
    "parameter",
}


VARIABLE_LIST_PARAMETERS = {
    "variables",
}


POINT_PARAMETERS = {
    "point",
    "point1",
    "point2",
    "center",
    "vertex",
    "origin",
    "start_point",
    "end_point",
}


VECTOR_PARAMETERS = {
    "vector",
    "direction",
}


BOUNDS_PARAMETERS = {
    "lower",
    "upper",
    "lower_bound",
    "upper_bound",
    "x_bounds",
    "y_bounds",
    "z_bounds",
    "r_bounds",
    "theta_bounds",
    "interval",
}


LIST_PARAMETERS = {
    "side_lengths",
    "intervals",
    "components",
    "field_components",
    "path_components",
    "position_components",
    "points",
}


MAPPING_PARAMETERS = {
    "substitutions",
}


STRING_PARAMETERS = {
    "unit",
    "output_unit",
    "function_name",
    "solve_for_rate",
    "angle_unit",
    "domain",

}


BOOLEAN_PARAMETERS = {
    "decimal",
}


# ============================================================
# OPERATION-SPECIFIC PARAMETER TYPE OVERRIDES
# ============================================================

# Global parameter names are useful, but some names mean different
# things in different deterministic operations. These overrides let
# SATURN interpret a parameter according to the selected operation
# without creating one-off parsers for every function.
OPERATION_PARAMETER_TYPE_OVERRIDES = {
    "absolute_extrema": {
        "start": "number",
        "end": "number",
    },
    "infinite_series_sum": {
        "start": "integer",
    },
    "partial_sum": {
        "start": "integer",
        "end": "integer",
    },
    "solve_trig_interval": {
        "start": "angle",
        "end": "angle",
    },
    "directional_derivative": {
        "direction": "vector",
    },
    "evaluate_limit": {
        "point": "number",
        "direction": "string",
    },
    "numerical_limit": {
        "point": "number",
    },
    "taylor_polynomial": {
        "center": "number",
    },
    "taylor_series": {
        "center": "number",
    },
    "differential_approximation": {
        "point": "number",
    },
    "discontinuity_type": {
        "point": "number",
    },
    "tangent_line": {
        "point": "number",
    },
    "normal_line": {
        "point": "number",
    },
    "point_to_line_distance": {
        "point_x": "number",
        "point_y": "number",
    },
}


# ============================================================
# PARAMETER TYPE LOOKUP
# ============================================================

def get_parameter_type(
    parameter_name,
    operation_name=None,
):
    """
    Return SATURN's language interpretation type for a
    deterministic function parameter.

    When an operation name is supplied, operation-specific
    overrides take priority over the global parameter schema.
    """

    name = str(parameter_name).lower()

    if operation_name is not None:

        operation_key = str(
            operation_name
        ).lower()

        operation_overrides = (
            OPERATION_PARAMETER_TYPE_OVERRIDES.get(
                operation_key,
                {},
            )
        )

        if name in operation_overrides:
            return operation_overrides[name]

    if name in NUMERIC_PARAMETERS:
        return "number"

    if name in INTEGER_PARAMETERS:
        return "integer"

    if name in ANGLE_PARAMETERS:
        return "angle"

    if name in EXPRESSION_PARAMETERS:
        return "expression"

    if name in EQUATION_PARAMETERS:
        return "equation"

    if name in EQUATION_LIST_PARAMETERS:
        return "equation_list"

    if name in VARIABLE_PARAMETERS:
        return "variable"

    if name in VARIABLE_LIST_PARAMETERS:
        return "variable_list"

    if name in POINT_PARAMETERS:
        return "point"

    if name in VECTOR_PARAMETERS:
        return "vector"

    if name in BOUNDS_PARAMETERS:
        return "bounds"

    if name in LIST_PARAMETERS:
        return "list"

    if name in MAPPING_PARAMETERS:
        return "mapping"

    if name in STRING_PARAMETERS:
        return "string"

    if name in BOOLEAN_PARAMETERS:
        return "boolean"

    return "unknown"


# ============================================================
# NATURAL-LANGUAGE ALIASES
# ============================================================

PARAMETER_ALIASES = {

    # --------------------------------------------------------
    # Geometry
    # --------------------------------------------------------

    "radius": [
        "radius",
        "r",
    ],

    "radius_1": [
        "radius 1",
        "first radius",
        "larger radius",
        "outer radius",
    ],

    "radius_2": [
        "radius 2",
        "second radius",
        "smaller radius",
        "inner radius",
    ],

    "inner_radius": [
        "inner radius",
        "inside radius",
        "smaller radius",
    ],

    "outer_radius": [
        "outer radius",
        "outside radius",
        "larger radius",
    ],

    "diameter": [
        "diameter",
    ],

    "length": [
        "length",
        "long",
    ],

    "width": [
        "width",
        "wide",
    ],

    "height": [
        "height",
        "high",
    ],

    "base": [
        "base",
    ],

    "base_1": [
        "base 1",
        "first base",
    ],

    "base_2": [
        "base 2",
        "second base",
    ],

    "side": [
        "side",
        "side length",
    ],

    "side_a": [
        "side a",
        "first side",
        "a side",
    ],

    "side_b": [
        "side b",
        "second side",
        "b side",
    ],

    "side_c": [
        "side c",
        "third side",
        "c side",
    ],

    "side_d": [
        "side d",
        "fourth side",
        "d side",
    ],

    "hypotenuse": [
        "hypotenuse",
    ],

    "opposite": [
        "opposite",
        "opposite side",
    ],

    "adjacent": [
        "adjacent",
        "adjacent side",
    ],

    "diagonal_1": [
        "diagonal 1",
        "first diagonal",
    ],

    "diagonal_2": [
        "diagonal 2",
        "second diagonal",
    ],

    "apothem": [
        "apothem",
    ],

    "slant_height": [
        "slant height",
    ],

    # --------------------------------------------------------
    # Coordinates
    # --------------------------------------------------------

    "x1": [
        "x1",
        "first x",
        "x coordinate of the first point",
    ],

    "y1": [
        "y1",
        "first y",
        "y coordinate of the first point",
    ],

    "x2": [
        "x2",
        "second x",
        "x coordinate of the second point",
    ],

    "y2": [
        "y2",
        "second y",
        "y coordinate of the second point",
    ],

    "x3": [
        "x3",
        "third x",
    ],

    "y3": [
        "y3",
        "third y",
    ],

    "center_x": [
        "center x",
        "x center",
        "x coordinate of the center",
    ],

    "center_y": [
        "center y",
        "y center",
        "y coordinate of the center",
    ],

    # --------------------------------------------------------
    # Angles
    # --------------------------------------------------------

    "angle": [
        "angle",
    ],

    "angle_a": [
        "angle a",
        "first angle",
    ],

    "angle_b": [
        "angle b",
        "second angle",
    ],

    "angle_c": [
        "angle c",
        "third angle",
    ],

    "degrees": [
        "degrees",
        "degree",
    ],

    "radians": [
        "radians",
        "radian",
    ],

    "bearing": [
        "bearing",
    ],

    # --------------------------------------------------------
    # Algebra / Calculus
    # --------------------------------------------------------

    "expression": [
        "expression",
        "function",
    ],

        "left_side": [
        "left side",
        "left hand side",
        "lhs",
    ],

    "right_side": [
        "right side",
        "right hand side",
        "rhs",
    ],

    "variable": [
        "variable",
        "with respect to",
        "in terms of",
    ],

    "lower": [
        "lower",
        "lower bound",
        "from",
    ],

    "upper": [
        "upper",
        "upper bound",
        "to",
    ],

    "lower_bound": [
        "lower bound",
        "lower limit",
        "from",
    ],

    "upper_bound": [
        "upper bound",
        "upper limit",
        "to",
    ],

    "x_bounds": [
        "x bounds",
        "x limits",
    ],

    "y_bounds": [
        "y bounds",
        "y limits",
    ],

    "z_bounds": [
        "z bounds",
        "z limits",
    ],

    "r_bounds": [
        "r bounds",
        "radial bounds",
        "r limits",
    ],

    "theta_bounds": [
        "theta bounds",
        "angular bounds",
        "theta limits",
    ],

    "interval": [
        "interval",
        "bounds",
        "range",
    ],

    "order": [
        "order",
    ],

    "degree": [
        "degree",
    ],

    # --------------------------------------------------------
    # Generic
    # --------------------------------------------------------

    "value": [
        "value",
        "number",
    ],

    "percentage": [
        "percentage",
        "percent",
    ],

    "scale_factor": [
        "scale factor",
    ],

    "number_of_sides": [
        "number of sides",
        "sides",
    ],

        "point": [
        "point",
        "at",
    ],

    "start_point": [
        "start point",
        "starting point",
        "initial point",
    ],

    "end_point": [
        "end point",
        "ending point",
        "final point",
    ],

    "direction": [
        "direction",
        "direction vector",
    ],

    "vector": [
        "vector",
    ],

    "components": [
        "components",
        "vector components",
    ],

    "field_components": [
        "field components",
        "vector field components",
    ],

    "path_components": [
        "path components",
        "path",
    ],

    "position_components": [
        "position components",
        "position vector components",
    ],

    "side_lengths": [
        "side lengths",
        "sides",
    ],

    "points": [
        "points",
        "vertices",
        "coordinates",
    ],

    "substitutions": [
        "substitutions",
        "substitution",
        "values",
        "replace",
    ],

    "unit": [
        "unit",
        "angle unit",
        "input unit",
    ],

    "output_unit": [
        "output unit",
        "result unit",
        "answer unit",
    ],

    "function_name": [
        "function name",
        "function",
    ],

    "solve_for_rate": [
        "solve for rate",
        "rate variable",
        "rate",
    ],

    "decimal": [
        "decimal",
        "decimal output",
        "decimal result",
        "as decimal",
    ],
}


# ============================================================
# ALIAS LOOKUP
# ============================================================

def get_parameter_aliases(parameter_name):
    """
    Return known natural-language aliases for a parameter.

    The real parameter name is always included automatically.
    Duplicate aliases are removed while preserving order.
    """

    name = str(parameter_name).lower()

    aliases = [
        name.replace("_", " "),
        *PARAMETER_ALIASES.get(
            name,
            []
        )
    ]

    unique_aliases = []

    for alias in aliases:
        if alias not in unique_aliases:
            unique_aliases.append(alias)

    return unique_aliases