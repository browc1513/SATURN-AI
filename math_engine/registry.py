# ============================================================
# N.O.V.A. MATH REGISTRY
# ============================================================

# ============================================================
# N.O.V.A. MATH REGISTRY
# ============================================================

import inspect

import math_engine.trigonometry as trigonometry_module
import math_engine.calculus as calculus_module

from math_engine.arithmetic import (
    add,
    subtract,
    multiply,
    divide,
    power,
    square_root,
    nth_root,
    absolute_value,
    factorial,
    greatest_common_divisor,
    least_common_multiple,
    percentage,
    percent_change,
    ratio,
    solve_proportion,
    prime_factorization,
    floor_value,
    ceiling_value,
    round_value,
    decimal_value,
    scientific_notation
)

from math_engine.algebra import (
    parse_expression,
    parse_variable,
    simplify_expression,
    expand_expression,
    factor_expression,
    substitute,
    solve_equation,
    find_roots,
    solve_system,
    solve_real,
    solve_inequality,
    polynomial_degree,
    polynomial_coefficients,
    quadratic_formula,
    complete_square,
    rational_simplify,
    combine_rational,
    partial_fraction,
    solve_exponential,
    solve_logarithmic,
    logarithm,
    find_domain,
    find_x_intercepts,
    find_y_intercept,
    inverse_function,
    polynomial_division,
    polynomial_remainder,
    polynomial_gcd,
    solve_absolute_value,
    evaluate_piecewise,
    solve_piecewise,
    get_numerator,
    get_denominator,
    leading_coefficient,
    polynomial_terms,
    detect_variables,
    solve_system_advanced,
    classify_system_solution,
    excluded_values,
    valid_domain,
    find_range
)

from math_engine.geometry import (
    rectangle_area,
    rectangle_perimeter,
    square_area,
    square_perimeter,
    triangle_area,
    triangle_perimeter,
    circle_area,
    circle_circumference,
    parallelogram_area,
    trapezoid_area,
    rhombus_area,
    distance_between_points,
    midpoint,
    slope,
    line_from_point_slope,
    line_from_two_points,
    are_parallel,
    are_perpendicular,
    pythagorean_hypotenuse,
    pythagorean_leg,
    triangle_is_valid,
    heron_triangle_area,
    missing_triangle_angle,
    classify_triangle_by_sides,
    classify_triangle_by_angles,
    circle_diameter,
    arc_length,
    sector_area,
    semicircle_area,
    annulus_area,
    regular_polygon_perimeter,
    regular_polygon_interior_angle,
    polygon_interior_angle_sum,
    regular_polygon_area_from_apothem,
    cube_volume,
    cube_surface_area,
    rectangular_prism_volume,
    rectangular_prism_surface_area,
    cylinder_volume,
    cylinder_surface_area,
    cone_volume,
    cone_surface_area,
    sphere_volume,
    sphere_surface_area,
    hemisphere_volume,
    hemisphere_surface_area,
    square_pyramid_volume,
    square_pyramid_surface_area,
    prism_volume,
    line_equation_slope_intercept,
    line_equation_point_slope,
    line_standard_form_from_points,
    line_x_intercept,
    line_y_intercept,
    line_intersection,
    point_to_line_distance,
    perpendicular_slope,
    perpendicular_bisector,
    triangle_angle_sum_is_valid,
    triangle_exterior_angle,
    classify_triangle_by_side_lengths,
    equilateral_triangle_height,
    equilateral_triangle_area,
    isosceles_triangle_height,
    isosceles_triangle_area,
    triangle_centroid,
    triangle_inradius_from_area,
    triangle_circumradius,
    circle_radius_from_diameter,
    circle_radius_from_circumference,
    circle_radius_from_area,
    circle_circumference_from_diameter,
    chord_length,
    center_to_chord_distance,
    circle_equation,
    circle_center_radius_from_standard,
    regular_polygon_exterior_angle,
    polygon_exterior_angle_sum,
    polygon_diagonals,
    regular_polygon_apothem,
    regular_polygon_area,
    regular_polygon_side_from_apothem,
    classify_polygon,
    polygon_perimeter,
    shoelace_area,
    rectangle_diagonal,
    square_diagonal,
    rhombus_perimeter,
    parallelogram_perimeter,
    trapezoid_perimeter,
    kite_area,
    kite_perimeter,
    quadrilateral_perimeter,
    translate_point,
    reflect_x_axis,
    reflect_y_axis,
    reflect_origin,
    rotate_point_90,
    rotate_point_180,
    rotate_point_270,
    rotate_point,
    dilate_point,
    dilate_point_about_center,
    translate_points,
    scale_factor,
    similar_figure_length,
    similar_figure_area,
    similar_figure_volume,
    triangular_prism_volume,
    triangular_prism_surface_area,
    prism_surface_area,
    pyramid_volume,
    rectangular_pyramid_volume,
    cone_slant_height,
    cylinder_lateral_area,
    cone_lateral_area,
    hemisphere_curved_surface_area,
    cone_frustum_volume,
    cone_frustum_surface_area,
    regular_tetrahedron_volume,
    regular_tetrahedron_surface_area
)


# ============================================================
# MATH REGISTRY CLASS
# ============================================================

class MathRegistry:
    """
    Central catalogue of deterministic math operations
    available to NOVA.
    """

    def __init__(self):
        self.operations = {}

    def register(
        self,
        name,
        function,
        subsystem,
        description,
        parameters=None,
        returns=None,
        keywords=None,
        category=None
    ):
        """
        Register one math operation.
        """

        if name in self.operations:
            raise ValueError(
                f"Operation '{name}' is already registered."
            )

        self.operations[name] = {
            "name": name,
            "function": function,
            "subsystem": subsystem,
            "description": description,
            "parameters": parameters or {},
            "returns": returns or {},
            "keywords": keywords or [],
            "category": category
        }

    def get(self, name):
        """
        Get one operation by exact registered name.
        """
        return self.operations.get(name)

    def exists(self, name):
        """
        Check whether an operation exists.
        """
        return name in self.operations

    def all_operations(self):
        """
        Return metadata for every registered operation.
        """
        return list(
            self.operations.values()
        )

    def names(self):
        """
        Return all registered operation names.
        """
        return list(
            self.operations.keys()
        )

    def by_subsystem(self, subsystem):
        """
        Return all operations belonging to a subsystem.
        """
        return [
            operation
            for operation in self.operations.values()
            if operation["subsystem"] == subsystem
        ]

    def by_category(self, category):
        """
        Return all operations belonging to a category.
        """
        return [
            operation
            for operation in self.operations.values()
            if operation["category"] == category
        ]

    def search(self, query):
        """
        Basic keyword search across operation metadata.
        """
        query = str(query).lower()

        results = []

        for operation in self.operations.values():

            searchable_text = " ".join(
                [
                    operation["name"],
                    operation["subsystem"],
                    operation["description"],
                    operation["category"] or "",
                    *operation["keywords"]
                ]
            ).lower()

            if query in searchable_text:
                results.append(operation)

        return results


# ============================================================
# ARITHMETIC REGISTRATION
# ============================================================

def register_arithmetic_operations(registry):
    """
    Register Arithmetic v1 operations.
    """

    registry.register(
        name="add",
        function=add,
        subsystem="arithmetic",
        description="Add two numbers.",
        parameters={
            "a": {
                "type": "number",
                "required": True,
                "description": "First number"
            },
            "b": {
                "type": "number",
                "required": True,
                "description": "Second number"
            }
        },
        returns={
            "type": "expression",
            "description": "Sum of the two numbers"
        },
        keywords=[
            "add",
            "addition",
            "sum",
            "plus",
            "total"
        ],
        category="basic_arithmetic"
    )

    registry.register(
        name="subtract",
        function=subtract,
        subsystem="arithmetic",
        description="Subtract one number from another.",
        parameters={
            "a": {
                "type": "number",
                "required": True,
                "description": "Starting value"
            },
            "b": {
                "type": "number",
                "required": True,
                "description": "Value to subtract"
            }
        },
        returns={
            "type": "expression",
            "description": "Difference between the values"
        },
        keywords=[
            "subtract",
            "subtraction",
            "minus",
            "difference"
        ],
        category="basic_arithmetic"
    )

    registry.register(
        name="multiply",
        function=multiply,
        subsystem="arithmetic",
        description="Multiply two numbers.",
        parameters={
            "a": {
                "type": "number",
                "required": True,
                "description": "First number"
            },
            "b": {
                "type": "number",
                "required": True,
                "description": "Second number"
            }
        },
        returns={
            "type": "expression",
            "description": "Product of the two numbers"
        },
        keywords=[
            "multiply",
            "multiplication",
            "times",
            "product"
        ],
        category="basic_arithmetic"
    )

    registry.register(
        name="divide",
        function=divide,
        subsystem="arithmetic",
        description="Divide one number by another.",
        parameters={
            "numerator": {
                "type": "number",
                "required": True,
                "description": "Value being divided"
            },
            "denominator": {
                "type": "number",
                "required": True,
                "description": "Value dividing the numerator"
            }
        },
        returns={
            "type": "expression",
            "description": "Quotient"
        },
        keywords=[
            "divide",
            "division",
            "quotient",
            "over"
        ],
        category="basic_arithmetic"
    )

    registry.register(
        name="power",
        function=power,
        subsystem="arithmetic",
        description="Raise a number to a power.",
        parameters={
            "base": {
                "type": "number",
                "required": True,
                "description": "Base value"
            },
            "exponent": {
                "type": "number",
                "required": True,
                "description": "Exponent"
            }
        },
        returns={
            "type": "expression",
            "description": "Base raised to the exponent"
        },
        keywords=[
            "power",
            "exponent",
            "raised",
            "squared",
            "cubed"
        ],
        category="powers_roots"
    )

    registry.register(
        name="square_root",
        function=square_root,
        subsystem="arithmetic",
        description="Calculate the square root of a number.",
        parameters={
            "value": {
                "type": "number",
                "required": True,
                "description": "Value whose square root is needed"
            }
        },
        returns={
            "type": "expression",
            "description": "Square root"
        },
        keywords=[
            "square root",
            "sqrt",
            "root"
        ],
        category="powers_roots"
    )

    registry.register(
        name="nth_root",
        function=nth_root,
        subsystem="arithmetic",
        description="Calculate the nth root of a number.",
        parameters={
            "value": {
                "type": "number",
                "required": True,
                "description": "Input value"
            },
            "n": {
                "type": "integer",
                "required": True,
                "description": "Root degree"
            }
        },
        returns={
            "type": "expression",
            "description": "Nth root"
        },
        keywords=[
            "nth root",
            "root",
            "cube root"
        ],
        category="powers_roots"
    )

    registry.register(
        name="absolute_value",
        function=absolute_value,
        subsystem="arithmetic",
        description="Calculate the absolute value of a number.",
        parameters={
            "value": {
                "type": "number",
                "required": True,
                "description": "Input value"
            }
        },
        returns={
            "type": "expression",
            "description": "Absolute value"
        },
        keywords=[
            "absolute value",
            "magnitude"
        ],
        category="basic_arithmetic"
    )

    registry.register(
        name="factorial",
        function=factorial,
        subsystem="arithmetic",
        description="Calculate the factorial of a nonnegative integer.",
        parameters={
            "value": {
                "type": "integer",
                "required": True,
                "description": "Nonnegative integer"
            }
        },
        returns={
            "type": "integer",
            "description": "Factorial"
        },
        keywords=[
            "factorial"
        ],
        category="integer_operations"
    )

    registry.register(
        name="greatest_common_divisor",
        function=greatest_common_divisor,
        subsystem="arithmetic",
        description="Find the greatest common divisor of two integers.",
        parameters={
            "a": {
                "type": "integer",
                "required": True,
                "description": "First integer"
            },
            "b": {
                "type": "integer",
                "required": True,
                "description": "Second integer"
            }
        },
        returns={
            "type": "integer",
            "description": "Greatest common divisor"
        },
        keywords=[
            "gcd",
            "greatest common divisor",
            "greatest common factor"
        ],
        category="integer_operations"
    )

    registry.register(
        name="least_common_multiple",
        function=least_common_multiple,
        subsystem="arithmetic",
        description="Find the least common multiple of two integers.",
        parameters={
            "a": {
                "type": "integer",
                "required": True,
                "description": "First integer"
            },
            "b": {
                "type": "integer",
                "required": True,
                "description": "Second integer"
            }
        },
        returns={
            "type": "integer",
            "description": "Least common multiple"
        },
        keywords=[
            "lcm",
            "least common multiple"
        ],
        category="integer_operations"
    )

    registry.register(
        name="percentage",
        function=percentage,
        subsystem="arithmetic",
        description="Calculate a percentage of a value.",
        parameters={
            "percent": {
                "type": "number",
                "required": True,
                "description": "Percentage"
            },
            "value": {
                "type": "number",
                "required": True,
                "description": "Value the percentage is taken from"
            }
        },
        returns={
            "type": "expression",
            "description": "Percentage of the value"
        },
        keywords=[
            "percentage",
            "percent",
            "of"
        ],
        category="percentages"
    )

    registry.register(
        name="percent_change",
        function=percent_change,
        subsystem="arithmetic",
        description="Calculate the percent change between two values.",
        parameters={
            "old_value": {
                "type": "number",
                "required": True,
                "description": "Original value"
            },
            "new_value": {
                "type": "number",
                "required": True,
                "description": "New value"
            }
        },
        returns={
            "type": "expression",
            "description": "Percent change"
        },
        keywords=[
            "percent change",
            "percentage change",
            "increase",
            "decrease"
        ],
        category="percentages"
    )

    registry.register(
        name="ratio",
        function=ratio,
        subsystem="arithmetic",
        description="Simplify a ratio between two values.",
        parameters={
            "a": {
                "type": "number",
                "required": True,
                "description": "First ratio value"
            },
            "b": {
                "type": "number",
                "required": True,
                "description": "Second ratio value"
            }
        },
        returns={
            "type": "expression",
            "description": "Simplified ratio"
        },
        keywords=[
            "ratio",
            "simplify ratio"
        ],
        category="ratios_proportions"
    )

    registry.register(
        name="solve_proportion",
        function=solve_proportion,
        subsystem="arithmetic",
        description="Solve a proportional relationship for an unknown.",
        parameters={
            "a": {
                "type": "number",
                "required": True,
                "description": "First numerator"
            },
            "b": {
                "type": "number",
                "required": True,
                "description": "First denominator"
            },
            "c": {
                "type": "number",
                "required": True,
                "description": "Second numerator"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Unknown value to solve for"
            }
        },
        returns={
            "type": "expression",
            "description": "Solution to the proportion"
        },
        keywords=[
            "proportion",
            "cross multiply",
            "ratio equation"
        ],
        category="ratios_proportions"
    )

    registry.register(
        name="prime_factorization",
        function=prime_factorization,
        subsystem="arithmetic",
        description="Find the prime factorization of an integer.",
        parameters={
            "value": {
                "type": "integer",
                "required": True,
                "description": "Integer to factor"
            }
        },
        returns={
            "type": "factorization",
            "description": "Prime factors and exponents"
        },
        keywords=[
            "prime factorization",
            "prime factors",
            "factor"
        ],
        category="integer_operations"
    )

    registry.register(
        name="floor_value",
        function=floor_value,
        subsystem="arithmetic",
        description="Calculate the floor of a number.",
        parameters={
            "value": {
                "type": "number",
                "required": True,
                "description": "Input number"
            }
        },
        returns={
            "type": "integer",
            "description": "Floor value"
        },
        keywords=[
            "floor",
            "round down"
        ],
        category="rounding"
    )

    registry.register(
        name="ceiling_value",
        function=ceiling_value,
        subsystem="arithmetic",
        description="Calculate the ceiling of a number.",
        parameters={
            "value": {
                "type": "number",
                "required": True,
                "description": "Input number"
            }
        },
        returns={
            "type": "integer",
            "description": "Ceiling value"
        },
        keywords=[
            "ceiling",
            "ceil",
            "round up"
        ],
        category="rounding"
    )

    registry.register(
        name="round_value",
        function=round_value,
        subsystem="arithmetic",
        description="Round a value to a specified number of decimal places.",
        parameters={
            "value": {
                "type": "number",
                "required": True,
                "description": "Input number"
            },
            "digits": {
                "type": "integer",
                "required": False,
                "description": "Number of decimal places"
            }
        },
        returns={
            "type": "number",
            "description": "Rounded value"
        },
        keywords=[
            "round",
            "rounded",
            "decimal places"
        ],
        category="rounding"
    )

    registry.register(
        name="decimal_value",
        function=decimal_value,
        subsystem="arithmetic",
        description="Convert an exact mathematical value to decimal form.",
        parameters={
            "value": {
                "type": "expression",
                "required": True,
                "description": "Exact value or expression"
            }
        },
        returns={
            "type": "number",
            "description": "Decimal approximation"
        },
        keywords=[
            "decimal",
            "approximate",
            "numerical value"
        ],
        category="numeric_conversion"
    )

    registry.register(
        name="scientific_notation",
        function=scientific_notation,
        subsystem="arithmetic",
        description="Express a number in scientific notation.",
        parameters={
            "value": {
                "type": "number",
                "required": True,
                "description": "Input number"
            }
        },
        returns={
            "type": "scientific_notation",
            "description": "Scientific notation representation"
        },
        keywords=[
            "scientific notation",
            "power of ten",
            "exponential notation"
        ],
        category="numeric_conversion"
    )


# ============================================================
# ALGEBRA REGISTRATION
# ============================================================

def register_algebra_operations(registry):
    """
    Register Algebra v1 operations.
    """

    registry.register(
        name="parse_expression",
        function=parse_expression,
        subsystem="algebra",
        description="Convert mathematical input into a symbolic expression.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Expression to parse"
            }
        },
        returns={
            "type": "expression",
            "description": "Parsed symbolic expression"
        },
        keywords=[
            "parse",
            "expression",
            "symbolic expression"
        ],
        category="algebra_utilities"
    )

    registry.register(
        name="parse_variable",
        function=parse_variable,
        subsystem="algebra",
        description="Convert a variable name into a symbolic variable.",
        parameters={
            "variable": {
                "type": "symbol",
                "required": True,
                "description": "Variable name"
            }
        },
        returns={
            "type": "symbol",
            "description": "Parsed symbolic variable"
        },
        keywords=[
            "variable",
            "symbol",
            "parse variable"
        ],
        category="algebra_utilities"
    )

    registry.register(
        name="simplify_expression",
        function=simplify_expression,
        subsystem="algebra",
        description="Simplify an algebraic expression.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Expression to simplify"
            }
        },
        returns={
            "type": "expression",
            "description": "Simplified expression"
        },
        keywords=[
            "simplify",
            "simplification",
            "reduce expression"
        ],
        category="expression_manipulation"
    )

    registry.register(
        name="expand_expression",
        function=expand_expression,
        subsystem="algebra",
        description="Expand products and powers in an algebraic expression.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Expression to expand"
            }
        },
        returns={
            "type": "expression",
            "description": "Expanded expression"
        },
        keywords=[
            "expand",
            "distribute",
            "foil"
        ],
        category="expression_manipulation"
    )

    registry.register(
        name="factor_expression",
        function=factor_expression,
        subsystem="algebra",
        description="Factor an algebraic expression.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Expression to factor"
            }
        },
        returns={
            "type": "expression",
            "description": "Factored expression"
        },
        keywords=[
            "factor",
            "factoring",
            "factor expression"
        ],
        category="expression_manipulation"
    )

    registry.register(
        name="substitute",
        function=substitute,
        subsystem="algebra",
        description="Substitute a value or expression for a variable.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Original expression"
            },
            "variable": {
                "type": "symbol",
                "required": True,
                "description": "Variable to replace"
            },
            "value": {
                "type": "expression",
                "required": True,
                "description": "Replacement value"
            }
        },
        returns={
            "type": "expression",
            "description": "Expression after substitution"
        },
        keywords=[
            "substitute",
            "plug in",
            "evaluate"
        ],
        category="expression_manipulation"
    )

    registry.register(
        name="solve_equation",
        function=solve_equation,
        subsystem="algebra",
        description="Solve an algebraic equation for a variable.",
        parameters={
            "left_side": {
                "type": "expression",
                "required": True,
                "description": "Left side of equation"
            },
            "right_side": {
                "type": "expression",
                "required": False,
                "description": "Right side of equation"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Variable to solve for"
            }
        },
        returns={
            "type": "solution_set",
            "description": "Solutions to the equation"
        },
        keywords=[
            "solve",
            "equation",
            "find x",
            "unknown"
        ],
        category="equations"
    )

    registry.register(
        name="find_roots",
        function=find_roots,
        subsystem="algebra",
        description="Find the roots or zeros of an expression.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Expression whose roots are needed"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Variable"
            }
        },
        returns={
            "type": "solution_set",
            "description": "Roots of the expression"
        },
        keywords=[
            "roots",
            "zeros",
            "solutions",
            "x intercepts"
        ],
        category="equations"
    )

    registry.register(
        name="solve_system",
        function=solve_system,
        subsystem="algebra",
        description="Solve a system of algebraic equations.",
        parameters={
            "equations": {
                "type": "equation_list",
                "required": True,
                "description": "Equations in the system"
            },
            "variables": {
                "type": "symbol_list",
                "required": True,
                "description": "Variables to solve for"
            }
        },
        returns={
            "type": "solution_set",
            "description": "Solutions to the system"
        },
        keywords=[
            "system",
            "simultaneous equations",
            "solve system"
        ],
        category="systems"
    )

    registry.register(
        name="solve_real",
        function=solve_real,
        subsystem="algebra",
        description="Solve an equation over the real numbers.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Equation or expression"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Variable to solve for"
            }
        },
        returns={
            "type": "solution_set",
            "description": "Real solutions"
        },
        keywords=[
            "real solutions",
            "solve real",
            "real roots"
        ],
        category="equations"
    )

    registry.register(
        name="solve_inequality",
        function=solve_inequality,
        subsystem="algebra",
        description="Solve an algebraic inequality.",
        parameters={
            "inequality": {
                "type": "expression",
                "required": True,
                "description": "Inequality to solve"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Variable"
            }
        },
        returns={
            "type": "set",
            "description": "Solution set of the inequality"
        },
        keywords=[
            "inequality",
            "greater than",
            "less than",
            "solve inequality"
        ],
        category="inequalities"
    )

    registry.register(
        name="polynomial_degree",
        function=polynomial_degree,
        subsystem="algebra",
        description="Determine the degree of a polynomial.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Polynomial expression"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Polynomial variable"
            }
        },
        returns={
            "type": "integer",
            "description": "Polynomial degree"
        },
        keywords=[
            "degree",
            "polynomial degree"
        ],
        category="polynomials"
    )

    registry.register(
        name="polynomial_coefficients",
        function=polynomial_coefficients,
        subsystem="algebra",
        description="Return the coefficients of a polynomial.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Polynomial expression"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Polynomial variable"
            }
        },
        returns={
            "type": "list",
            "description": "Polynomial coefficients"
        },
        keywords=[
            "coefficients",
            "polynomial coefficients"
        ],
        category="polynomials"
    )

    registry.register(
        name="quadratic_formula",
        function=quadratic_formula,
        subsystem="algebra",
        description="Solve a quadratic equation using the quadratic formula.",
        parameters={
            "a": {
                "type": "number",
                "required": True,
                "description": "Quadratic coefficient"
            },
            "b": {
                "type": "number",
                "required": True,
                "description": "Linear coefficient"
            },
            "c": {
                "type": "number",
                "required": True,
                "description": "Constant coefficient"
            }
        },
        returns={
            "type": "solution_set",
            "description": "Quadratic solutions"
        },
        keywords=[
            "quadratic formula",
            "quadratic",
            "roots"
        ],
        category="polynomials"
    )

    registry.register(
        name="complete_square",
        function=complete_square,
        subsystem="algebra",
        description="Rewrite a quadratic expression by completing the square.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Quadratic expression"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Variable"
            }
        },
        returns={
            "type": "expression",
            "description": "Completed-square form"
        },
        keywords=[
            "complete square",
            "completing the square",
            "vertex form"
        ],
        category="polynomials"
    )

    registry.register(
        name="rational_simplify",
        function=rational_simplify,
        subsystem="algebra",
        description="Simplify a rational algebraic expression.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Rational expression"
            }
        },
        returns={
            "type": "expression",
            "description": "Simplified rational expression"
        },
        keywords=[
            "rational expression",
            "simplify fraction",
            "cancel"
        ],
        category="rational_expressions"
    )

    registry.register(
        name="combine_rational",
        function=combine_rational,
        subsystem="algebra",
        description="Combine rational terms into a single fraction.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Rational expression"
            }
        },
        returns={
            "type": "expression",
            "description": "Combined rational expression"
        },
        keywords=[
            "combine fractions",
            "common denominator",
            "rational"
        ],
        category="rational_expressions"
    )

    registry.register(
        name="partial_fraction",
        function=partial_fraction,
        subsystem="algebra",
        description="Decompose a rational expression into partial fractions.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Rational expression"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Variable"
            }
        },
        returns={
            "type": "expression",
            "description": "Partial fraction decomposition"
        },
        keywords=[
            "partial fractions",
            "decompose fraction"
        ],
        category="rational_expressions"
    )

    registry.register(
        name="solve_exponential",
        function=solve_exponential,
        subsystem="algebra",
        description="Solve an exponential equation.",
        parameters={
            "equation": {
                "type": "expression",
                "required": True,
                "description": "Exponential equation"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Variable"
            }
        },
        returns={
            "type": "solution_set",
            "description": "Solutions to the exponential equation"
        },
        keywords=[
            "exponential equation",
            "solve exponential"
        ],
        category="exponential_logarithmic"
    )

    registry.register(
        name="solve_logarithmic",
        function=solve_logarithmic,
        subsystem="algebra",
        description="Solve a logarithmic equation.",
        parameters={
            "equation": {
                "type": "expression",
                "required": True,
                "description": "Logarithmic equation"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Variable"
            }
        },
        returns={
            "type": "solution_set",
            "description": "Solutions to the logarithmic equation"
        },
        keywords=[
            "log equation",
            "logarithmic equation",
            "solve logarithm"
        ],
        category="exponential_logarithmic"
    )

    registry.register(
        name="logarithm",
        function=logarithm,
        subsystem="algebra",
        description="Evaluate a logarithm with an optional base.",
        parameters={
            "value": {
                "type": "number",
                "required": True,
                "description": "Logarithm argument"
            },
            "base": {
                "type": "number",
                "required": False,
                "description": "Logarithm base"
            }
        },
        returns={
            "type": "expression",
            "description": "Logarithm value"
        },
        keywords=[
            "log",
            "logarithm",
            "natural log"
        ],
        category="exponential_logarithmic"
    )

    registry.register(
        name="find_domain",
        function=find_domain,
        subsystem="algebra",
        description="Determine the domain of an expression.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Expression"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Variable"
            }
        },
        returns={
            "type": "set",
            "description": "Domain of the expression"
        },
        keywords=[
            "domain",
            "allowed values",
            "function domain"
        ],
        category="functions"
    )

    registry.register(
        name="find_x_intercepts",
        function=find_x_intercepts,
        subsystem="algebra",
        description="Find the x-intercepts of a function.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Function expression"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Independent variable"
            }
        },
        returns={
            "type": "solution_set",
            "description": "X-intercepts"
        },
        keywords=[
            "x intercept",
            "x intercepts",
            "zeros",
            "roots"
        ],
        category="functions"
    )

    registry.register(
        name="find_y_intercept",
        function=find_y_intercept,
        subsystem="algebra",
        description="Find the y-intercept of a function.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Function expression"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Independent variable"
            }
        },
        returns={
            "type": "expression",
            "description": "Y-intercept"
        },
        keywords=[
            "y intercept",
            "y intercepts"
        ],
        category="functions"
    )

    registry.register(
        name="inverse_function",
        function=inverse_function,
        subsystem="algebra",
        description="Find the inverse of a function.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Function expression"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Input variable"
            }
        },
        returns={
            "type": "expression",
            "description": "Inverse function"
        },
        keywords=[
            "inverse",
            "inverse function"
        ],
        category="functions"
    )

    registry.register(
        name="polynomial_division",
        function=polynomial_division,
        subsystem="algebra",
        description="Divide one polynomial by another.",
        parameters={
            "dividend": {
                "type": "expression",
                "required": True,
                "description": "Polynomial being divided"
            },
            "divisor": {
                "type": "expression",
                "required": True,
                "description": "Polynomial divisor"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Polynomial variable"
            }
        },
        returns={
            "type": "tuple",
            "description": "Polynomial quotient and remainder"
        },
        keywords=[
            "polynomial division",
            "long division",
            "divide polynomial"
        ],
        category="polynomials"
    )

    registry.register(
        name="polynomial_remainder",
        function=polynomial_remainder,
        subsystem="algebra",
        description="Find the remainder from polynomial division.",
        parameters={
            "dividend": {
                "type": "expression",
                "required": True,
                "description": "Polynomial being divided"
            },
            "divisor": {
                "type": "expression",
                "required": True,
                "description": "Polynomial divisor"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Polynomial variable"
            }
        },
        returns={
            "type": "expression",
            "description": "Polynomial remainder"
        },
        keywords=[
            "remainder",
            "polynomial remainder"
        ],
        category="polynomials"
    )

    registry.register(
        name="polynomial_gcd",
        function=polynomial_gcd,
        subsystem="algebra",
        description="Find the greatest common divisor of two polynomials.",
        parameters={
            "first": {
                "type": "expression",
                "required": True,
                "description": "First polynomial"
            },
            "second": {
                "type": "expression",
                "required": True,
                "description": "Second polynomial"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Polynomial variable"
            }
        },
        returns={
            "type": "expression",
            "description": "Polynomial greatest common divisor"
        },
        keywords=[
            "polynomial gcd",
            "greatest common divisor",
            "common polynomial factor"
        ],
        category="polynomials"
    )

    registry.register(
        name="solve_absolute_value",
        function=solve_absolute_value,
        subsystem="algebra",
        description="Solve an equation containing absolute values.",
        parameters={
            "left_side": {
                "type": "expression",
                "required": True,
                "description": "Left side of equation"
            },
            "right_side": {
                "type": "expression",
                "required": False,
                "description": "Right side of equation"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Variable"
            }
        },
        returns={
            "type": "solution_set",
            "description": "Solutions to the absolute-value equation"
        },
        keywords=[
            "absolute value equation",
            "solve absolute value"
        ],
        category="equations"
    )

    registry.register(
        name="evaluate_piecewise",
        function=evaluate_piecewise,
        subsystem="algebra",
        description="Evaluate a piecewise-defined function at a value.",
        parameters={
            "expression": {
                "type": "piecewise_expression",
                "required": True,
                "description": "Piecewise expression"
            },
            "variable": {
                "type": "symbol",
                "required": True,
                "description": "Independent variable"
            },
            "value": {
                "type": "number",
                "required": True,
                "description": "Value at which to evaluate"
            }
        },
        returns={
            "type": "expression",
            "description": "Piecewise function value"
        },
        keywords=[
            "piecewise",
            "evaluate piecewise"
        ],
        category="piecewise"
    )

    registry.register(
        name="solve_piecewise",
        function=solve_piecewise,
        subsystem="algebra",
        description="Solve an equation involving a piecewise expression.",
        parameters={
            "expression": {
                "type": "piecewise_expression",
                "required": True,
                "description": "Piecewise expression"
            },
            "right_side": {
                "type": "expression",
                "required": False,
                "description": "Right side of equation"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Variable"
            }
        },
        returns={
            "type": "solution_set",
            "description": "Piecewise equation solutions"
        },
        keywords=[
            "solve piecewise",
            "piecewise equation"
        ],
        category="piecewise"
    )

    registry.register(
        name="get_numerator",
        function=get_numerator,
        subsystem="algebra",
        description="Extract the numerator of a rational expression.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Rational expression"
            }
        },
        returns={
            "type": "expression",
            "description": "Numerator"
        },
        keywords=[
            "numerator",
            "top of fraction"
        ],
        category="rational_expressions"
    )

    registry.register(
        name="get_denominator",
        function=get_denominator,
        subsystem="algebra",
        description="Extract the denominator of a rational expression.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Rational expression"
            }
        },
        returns={
            "type": "expression",
            "description": "Denominator"
        },
        keywords=[
            "denominator",
            "bottom of fraction"
        ],
        category="rational_expressions"
    )

    registry.register(
        name="leading_coefficient",
        function=leading_coefficient,
        subsystem="algebra",
        description="Find the leading coefficient of a polynomial.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Polynomial expression"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Polynomial variable"
            }
        },
        returns={
            "type": "expression",
            "description": "Leading coefficient"
        },
        keywords=[
            "leading coefficient",
            "highest degree coefficient"
        ],
        category="polynomials"
    )

    registry.register(
        name="polynomial_terms",
        function=polynomial_terms,
        subsystem="algebra",
        description="Return the terms of a polynomial.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Polynomial expression"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Polynomial variable"
            }
        },
        returns={
            "type": "list",
            "description": "Polynomial terms"
        },
        keywords=[
            "polynomial terms",
            "terms"
        ],
        category="polynomials"
    )

    registry.register(
        name="detect_variables",
        function=detect_variables,
        subsystem="algebra",
        description="Detect symbolic variables contained in an expression.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Expression to inspect"
            }
        },
        returns={
            "type": "symbol_list",
            "description": "Variables found in the expression"
        },
        keywords=[
            "detect variables",
            "variables",
            "symbols"
        ],
        category="algebra_utilities"
    )

    registry.register(
        name="solve_system_advanced",
        function=solve_system_advanced,
        subsystem="algebra",
        description="Solve and analyze a more general system of equations.",
        parameters={
            "equations": {
                "type": "equation_list",
                "required": True,
                "description": "System equations"
            },
            "variables": {
                "type": "symbol_list",
                "required": True,
                "description": "Variables"
            }
        },
        returns={
            "type": "solution_set",
            "description": "System solution information"
        },
        keywords=[
            "advanced system",
            "solve system",
            "simultaneous equations"
        ],
        category="systems"
    )

    registry.register(
        name="classify_system_solution",
        function=classify_system_solution,
        subsystem="algebra",
        description="Classify a system as having a unique solution, infinitely many solutions, or no solution.",
        parameters={
            "solution": {
                "type": "solution",
                "required": True,
                "description": "System solution data"
            },
            "variables": {
                "type": "symbol_list",
                "required": False,
                "description": "System variables"
            }
        },
        returns={
            "type": "string",
            "description": "System solution classification"
        },
        keywords=[
            "classify system",
            "unique solution",
            "infinite solutions",
            "no solution"
        ],
        category="systems"
    )

    registry.register(
        name="excluded_values",
        function=excluded_values,
        subsystem="algebra",
        description="Find values excluded from the domain of a rational expression.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Expression"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Variable"
            }
        },
        returns={
            "type": "set",
            "description": "Excluded values"
        },
        keywords=[
            "excluded values",
            "restrictions",
            "undefined values"
        ],
        category="functions"
    )

    registry.register(
        name="valid_domain",
        function=valid_domain,
        subsystem="algebra",
        description="Determine the valid real domain of an expression.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Expression"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Variable"
            }
        },
        returns={
            "type": "set",
            "description": "Valid domain"
        },
        keywords=[
            "valid domain",
            "domain",
            "restrictions"
        ],
        category="functions"
    )

    registry.register(
        name="find_range",
        function=find_range,
        subsystem="algebra",
        description="Determine the range of a function.",
        parameters={
            "expression": {
                "type": "expression",
                "required": True,
                "description": "Function expression"
            },
            "variable": {
                "type": "symbol",
                "required": False,
                "description": "Independent variable"
            }
        },
        returns={
            "type": "set",
            "description": "Range of the function"
        },
        keywords=[
            "range",
            "function range",
            "output values"
        ],
        category="functions"
    )


# ============================================================
# GEOMETRY REGISTRATION
# ============================================================

def register_geometry_operations(registry):
    """
    Register Geometry v1 operations.
    """

    geometry_operations = [
        # ----------------------------------------------------
        # BASIC 2D GEOMETRY
        # ----------------------------------------------------
        (rectangle_area, "Calculate the area of a rectangle.", ["rectangle", "area", "length", "width"], "2d_geometry"),
        (rectangle_perimeter, "Calculate the perimeter of a rectangle.", ["rectangle", "perimeter", "length", "width"], "2d_geometry"),
        (square_area, "Calculate the area of a square.", ["square", "area", "side"], "2d_geometry"),
        (square_perimeter, "Calculate the perimeter of a square.", ["square", "perimeter", "side"], "2d_geometry"),
        (triangle_area, "Calculate triangle area from base and height.", ["triangle", "area", "base", "height"], "triangle_geometry"),
        (triangle_perimeter, "Calculate the perimeter of a triangle.", ["triangle", "perimeter", "sides"], "triangle_geometry"),
        (circle_area, "Calculate the area of a circle.", ["circle", "area", "radius"], "circle_geometry"),
        (circle_circumference, "Calculate the circumference of a circle.", ["circle", "circumference", "radius"], "circle_geometry"),
        (parallelogram_area, "Calculate the area of a parallelogram.", ["parallelogram", "area", "base", "height"], "2d_geometry"),
        (trapezoid_area, "Calculate the area of a trapezoid.", ["trapezoid", "area", "bases", "height"], "2d_geometry"),
        (rhombus_area, "Calculate the area of a rhombus.", ["rhombus", "area", "diagonals"], "2d_geometry"),

        # ----------------------------------------------------
        # COORDINATE GEOMETRY
        # ----------------------------------------------------
        (distance_between_points, "Calculate the distance between two points.", ["distance", "points", "coordinates"], "coordinate_geometry"),
        (midpoint, "Find the midpoint between two points.", ["midpoint", "points", "coordinates"], "coordinate_geometry"),
        (slope, "Calculate the slope between two points.", ["slope", "rise", "run", "points"], "coordinate_geometry"),
        (line_from_point_slope, "Construct a line from a point and slope.", ["line", "point slope", "slope"], "coordinate_geometry"),
        (line_from_two_points, "Construct a line through two points.", ["line", "two points", "equation"], "coordinate_geometry"),
        (are_parallel, "Determine whether two lines or slopes are parallel.", ["parallel", "lines", "slopes"], "coordinate_geometry"),
        (are_perpendicular, "Determine whether two lines or slopes are perpendicular.", ["perpendicular", "lines", "slopes"], "coordinate_geometry"),

        # ----------------------------------------------------
        # TRIANGLES
        # ----------------------------------------------------
        (pythagorean_hypotenuse, "Calculate the hypotenuse of a right triangle.", ["pythagorean", "hypotenuse", "right triangle"], "triangle_geometry"),
        (pythagorean_leg, "Calculate a missing leg of a right triangle.", ["pythagorean", "leg", "right triangle"], "triangle_geometry"),
        (triangle_is_valid, "Determine whether three side lengths form a valid triangle.", ["triangle", "valid", "triangle inequality"], "triangle_geometry"),
        (heron_triangle_area, "Calculate triangle area using Heron's formula.", ["heron", "triangle", "area", "three sides"], "triangle_geometry"),
        (missing_triangle_angle, "Calculate the missing angle of a triangle.", ["triangle", "missing angle", "angle sum"], "triangle_geometry"),
        (classify_triangle_by_sides, "Classify a triangle by its sides.", ["triangle", "equilateral", "isosceles", "scalene"], "triangle_geometry"),
        (classify_triangle_by_angles, "Classify a triangle by its angles.", ["triangle", "acute", "right", "obtuse"], "triangle_geometry"),

        # ----------------------------------------------------
        # CIRCLES
        # ----------------------------------------------------
        (circle_diameter, "Calculate a circle's diameter from its radius.", ["circle", "diameter", "radius"], "circle_geometry"),
        (arc_length, "Calculate the length of a circular arc.", ["circle", "arc", "arc length"], "circle_geometry"),
        (sector_area, "Calculate the area of a circular sector.", ["circle", "sector", "area"], "circle_geometry"),
        (semicircle_area, "Calculate the area of a semicircle.", ["circle", "semicircle", "area"], "circle_geometry"),
        (annulus_area, "Calculate the area of an annulus.", ["circle", "annulus", "ring", "area"], "circle_geometry"),

        # ----------------------------------------------------
        # POLYGONS
        # ----------------------------------------------------
        (regular_polygon_perimeter, "Calculate the perimeter of a regular polygon.", ["polygon", "regular", "perimeter"], "polygon_geometry"),
        (regular_polygon_interior_angle, "Calculate each interior angle of a regular polygon.", ["polygon", "interior angle", "regular"], "polygon_geometry"),
        (polygon_interior_angle_sum, "Calculate the sum of a polygon's interior angles.", ["polygon", "interior angles", "angle sum"], "polygon_geometry"),
        (regular_polygon_area_from_apothem, "Calculate regular polygon area from apothem and perimeter.", ["polygon", "apothem", "area"], "polygon_geometry"),

        # ----------------------------------------------------
        # BASIC 3D GEOMETRY
        # ----------------------------------------------------
        (cube_volume, "Calculate the volume of a cube.", ["cube", "volume"], "solid_geometry"),
        (cube_surface_area, "Calculate the surface area of a cube.", ["cube", "surface area"], "solid_geometry"),
        (rectangular_prism_volume, "Calculate rectangular prism volume.", ["rectangular prism", "volume"], "solid_geometry"),
        (rectangular_prism_surface_area, "Calculate rectangular prism surface area.", ["rectangular prism", "surface area"], "solid_geometry"),
        (cylinder_volume, "Calculate cylinder volume.", ["cylinder", "volume"], "solid_geometry"),
        (cylinder_surface_area, "Calculate cylinder surface area.", ["cylinder", "surface area"], "solid_geometry"),
        (cone_volume, "Calculate cone volume.", ["cone", "volume"], "solid_geometry"),
        (cone_surface_area, "Calculate cone surface area.", ["cone", "surface area"], "solid_geometry"),
        (sphere_volume, "Calculate sphere volume.", ["sphere", "volume"], "solid_geometry"),
        (sphere_surface_area, "Calculate sphere surface area.", ["sphere", "surface area"], "solid_geometry"),
        (hemisphere_volume, "Calculate hemisphere volume.", ["hemisphere", "volume"], "solid_geometry"),
        (hemisphere_surface_area, "Calculate hemisphere surface area.", ["hemisphere", "surface area"], "solid_geometry"),
        (square_pyramid_volume, "Calculate square pyramid volume.", ["square pyramid", "volume"], "solid_geometry"),
        (square_pyramid_surface_area, "Calculate square pyramid surface area.", ["square pyramid", "surface area"], "solid_geometry"),
        (prism_volume, "Calculate the volume of a prism.", ["prism", "volume", "base area"], "solid_geometry"),

        # ----------------------------------------------------
        # LINE GEOMETRY
        # ----------------------------------------------------
        (line_equation_slope_intercept, "Construct a line in slope-intercept form.", ["line", "slope intercept", "y=mx+b"], "line_geometry"),
        (line_equation_point_slope, "Construct a line in point-slope form.", ["line", "point slope"], "line_geometry"),
        (line_standard_form_from_points, "Construct a line in standard form from two points.", ["line", "standard form", "two points"], "line_geometry"),
        (line_x_intercept, "Find the x-intercept of a line.", ["line", "x intercept"], "line_geometry"),
        (line_y_intercept, "Find the y-intercept of a line.", ["line", "y intercept"], "line_geometry"),
        (line_intersection, "Find the intersection of two lines.", ["lines", "intersection"], "line_geometry"),
        (point_to_line_distance, "Calculate the distance from a point to a line.", ["point", "line", "distance"], "line_geometry"),
        (perpendicular_slope, "Calculate the slope perpendicular to a given slope.", ["perpendicular", "slope"], "line_geometry"),
        (perpendicular_bisector, "Find the perpendicular bisector of a segment.", ["perpendicular bisector", "segment", "midpoint"], "line_geometry"),

        # ----------------------------------------------------
        # ADVANCED TRIANGLE GEOMETRY
        # ----------------------------------------------------
        (triangle_angle_sum_is_valid, "Check whether three angles form a valid triangle.", ["triangle", "angles", "valid"], "triangle_geometry"),
        (triangle_exterior_angle, "Calculate a triangle exterior angle.", ["triangle", "exterior angle"], "triangle_geometry"),
        (classify_triangle_by_side_lengths, "Classify a triangle using side lengths.", ["triangle", "side lengths", "classify"], "triangle_geometry"),
        (equilateral_triangle_height, "Calculate the height of an equilateral triangle.", ["equilateral", "triangle", "height"], "triangle_geometry"),
        (equilateral_triangle_area, "Calculate the area of an equilateral triangle.", ["equilateral", "triangle", "area"], "triangle_geometry"),
        (isosceles_triangle_height, "Calculate the height of an isosceles triangle.", ["isosceles", "triangle", "height"], "triangle_geometry"),
        (isosceles_triangle_area, "Calculate the area of an isosceles triangle.", ["isosceles", "triangle", "area"], "triangle_geometry"),
        (triangle_centroid, "Calculate the centroid of a triangle.", ["triangle", "centroid"], "triangle_geometry"),
        (triangle_inradius_from_area, "Calculate triangle inradius from area and semiperimeter.", ["triangle", "inradius", "incircle"], "triangle_geometry"),
        (triangle_circumradius, "Calculate the circumradius of a triangle.", ["triangle", "circumradius", "circumcircle"], "triangle_geometry"),

        # ----------------------------------------------------
        # ADVANCED CIRCLE GEOMETRY
        # ----------------------------------------------------
        (circle_radius_from_diameter, "Calculate circle radius from diameter.", ["circle", "radius", "diameter"], "circle_geometry"),
        (circle_radius_from_circumference, "Calculate circle radius from circumference.", ["circle", "radius", "circumference"], "circle_geometry"),
        (circle_radius_from_area, "Calculate circle radius from area.", ["circle", "radius", "area"], "circle_geometry"),
        (circle_circumference_from_diameter, "Calculate circumference from diameter.", ["circle", "circumference", "diameter"], "circle_geometry"),
        (chord_length, "Calculate the length of a circle chord.", ["circle", "chord", "length"], "circle_geometry"),
        (center_to_chord_distance, "Calculate distance from circle center to a chord.", ["circle", "chord", "center", "distance"], "circle_geometry"),
        (circle_equation, "Construct the equation of a circle.", ["circle", "equation", "center", "radius"], "circle_geometry"),
        (circle_center_radius_from_standard, "Extract a circle's center and radius from its equation.", ["circle", "center", "radius", "equation"], "circle_geometry"),

        # ----------------------------------------------------
        # ADVANCED POLYGONS
        # ----------------------------------------------------
        (regular_polygon_exterior_angle, "Calculate each exterior angle of a regular polygon.", ["polygon", "exterior angle"], "polygon_geometry"),
        (polygon_exterior_angle_sum, "Calculate the exterior-angle sum of a polygon.", ["polygon", "exterior angles", "angle sum"], "polygon_geometry"),
        (polygon_diagonals, "Calculate the number of diagonals in a polygon.", ["polygon", "diagonals"], "polygon_geometry"),
        (regular_polygon_apothem, "Calculate the apothem of a regular polygon.", ["polygon", "apothem"], "polygon_geometry"),
        (regular_polygon_area, "Calculate the area of a regular polygon.", ["polygon", "regular", "area"], "polygon_geometry"),
        (regular_polygon_side_from_apothem, "Calculate regular polygon side length from its apothem.", ["polygon", "apothem", "side length"], "polygon_geometry"),
        (classify_polygon, "Classify a polygon by its number of sides.", ["polygon", "classify", "sides"], "polygon_geometry"),
        (polygon_perimeter, "Calculate a polygon's perimeter from its side lengths.", ["polygon", "perimeter", "sides"], "polygon_geometry"),
        (shoelace_area, "Calculate polygon area using the shoelace formula.", ["polygon", "shoelace", "coordinates", "area"], "polygon_geometry"),

        # ----------------------------------------------------
        # QUADRILATERALS
        # ----------------------------------------------------
        (rectangle_diagonal, "Calculate the diagonal of a rectangle.", ["rectangle", "diagonal"], "quadrilateral_geometry"),
        (square_diagonal, "Calculate the diagonal of a square.", ["square", "diagonal"], "quadrilateral_geometry"),
        (rhombus_perimeter, "Calculate the perimeter of a rhombus.", ["rhombus", "perimeter"], "quadrilateral_geometry"),
        (parallelogram_perimeter, "Calculate the perimeter of a parallelogram.", ["parallelogram", "perimeter"], "quadrilateral_geometry"),
        (trapezoid_perimeter, "Calculate the perimeter of a trapezoid.", ["trapezoid", "perimeter"], "quadrilateral_geometry"),
        (kite_area, "Calculate the area of a kite.", ["kite", "area", "diagonals"], "quadrilateral_geometry"),
        (kite_perimeter, "Calculate the perimeter of a kite.", ["kite", "perimeter"], "quadrilateral_geometry"),
        (quadrilateral_perimeter, "Calculate the perimeter of a quadrilateral.", ["quadrilateral", "perimeter"], "quadrilateral_geometry"),

        # ----------------------------------------------------
        # TRANSFORMATIONS
        # ----------------------------------------------------
        (translate_point, "Translate a point in the coordinate plane.", ["translate", "translation", "point"], "transformations"),
        (reflect_x_axis, "Reflect a point across the x-axis.", ["reflect", "x axis"], "transformations"),
        (reflect_y_axis, "Reflect a point across the y-axis.", ["reflect", "y axis"], "transformations"),
        (reflect_origin, "Reflect a point through the origin.", ["reflect", "origin"], "transformations"),
        (rotate_point_90, "Rotate a point 90 degrees.", ["rotate", "rotation", "90 degrees"], "transformations"),
        (rotate_point_180, "Rotate a point 180 degrees.", ["rotate", "rotation", "180 degrees"], "transformations"),
        (rotate_point_270, "Rotate a point 270 degrees.", ["rotate", "rotation", "270 degrees"], "transformations"),
        (rotate_point, "Rotate a point by an arbitrary angle.", ["rotate", "rotation", "point", "angle"], "transformations"),
        (dilate_point, "Dilate a point about the origin.", ["dilate", "dilation", "scale factor"], "transformations"),
        (dilate_point_about_center, "Dilate a point about a specified center.", ["dilate", "dilation", "center", "scale factor"], "transformations"),
        (translate_points, "Translate multiple points.", ["translate", "points", "translation"], "transformations"),

        # ----------------------------------------------------
        # SIMILARITY
        # ----------------------------------------------------
        (scale_factor, "Calculate the scale factor between similar figures.", ["scale factor", "similar figures"], "similarity"),
        (similar_figure_length, "Calculate a corresponding length in similar figures.", ["similar figures", "length", "scale factor"], "similarity"),
        (similar_figure_area, "Calculate corresponding area using a scale factor.", ["similar figures", "area", "scale factor"], "similarity"),
        (similar_figure_volume, "Calculate corresponding volume using a scale factor.", ["similar figures", "volume", "scale factor"], "similarity"),

        # ----------------------------------------------------
        # ADVANCED SOLID GEOMETRY
        # ----------------------------------------------------
        (triangular_prism_volume, "Calculate triangular prism volume.", ["triangular prism", "volume"], "solid_geometry"),
        (triangular_prism_surface_area, "Calculate triangular prism surface area.", ["triangular prism", "surface area"], "solid_geometry"),
        (prism_surface_area, "Calculate prism surface area.", ["prism", "surface area"], "solid_geometry"),
        (pyramid_volume, "Calculate pyramid volume.", ["pyramid", "volume"], "solid_geometry"),
        (rectangular_pyramid_volume, "Calculate rectangular pyramid volume.", ["rectangular pyramid", "volume"], "solid_geometry"),
        (cone_slant_height, "Calculate the slant height of a cone.", ["cone", "slant height"], "solid_geometry"),
        (cylinder_lateral_area, "Calculate the lateral area of a cylinder.", ["cylinder", "lateral area"], "solid_geometry"),
        (cone_lateral_area, "Calculate the lateral area of a cone.", ["cone", "lateral area"], "solid_geometry"),
        (hemisphere_curved_surface_area, "Calculate the curved surface area of a hemisphere.", ["hemisphere", "curved surface area"], "solid_geometry"),
        (cone_frustum_volume, "Calculate the volume of a conical frustum.", ["cone", "frustum", "volume"], "solid_geometry"),
        (cone_frustum_surface_area, "Calculate the surface area of a conical frustum.", ["cone", "frustum", "surface area"], "solid_geometry"),
        (regular_tetrahedron_volume, "Calculate regular tetrahedron volume.", ["tetrahedron", "volume"], "solid_geometry"),
        (regular_tetrahedron_surface_area, "Calculate regular tetrahedron surface area.", ["tetrahedron", "surface area"], "solid_geometry"),
    ]

    for function, description, keywords, category in geometry_operations:
        registry.register(
            name=function.__name__,
            function=function,
            subsystem="geometry",
            description=description,
            parameters={
                "dynamic": {
                    "type": "function_signature",
                    "required": True,
                    "description": "Parameters defined by the deterministic geometry function."
                }
            },
            returns={
                "type": "expression",
                "description": "Geometry operation result."
            },
            keywords=keywords,
            category=category
        )


# ============================================================
# TRIGONOMETRY REGISTRATION
# ============================================================

def _trig_category(function_name):
    """
    Infer a Trigonometry category from a function name.
    """

    name = function_name.lower()

    if "degree" in name or "radian" in name or "angle" in name:
        return "angle_fundamentals"

    if "inverse" in name or "asin" in name or "acos" in name or "atan" in name:
        return "inverse_trigonometry"

    if "unit_circle" in name:
        return "unit_circle"

    if (
        "right_triangle" in name
        or "opposite" in name
        or "adjacent" in name
        or "hypotenuse" in name
    ):
        return "right_triangle_trigonometry"

    if "identity" in name or "simplify" in name or "rewrite" in name:
        return "trigonometric_identities"

    if (
        "double_angle" in name
        or "half_angle" in name
        or "sum_angle" in name
        or "difference_angle" in name
    ):
        return "angle_identities"

    if "solve" in name and "triangle" not in name:
        return "trigonometric_equations"

    if (
        "amplitude" in name
        or "period" in name
        or "phase" in name
        or "frequency" in name
    ):
        return "trigonometric_graphs"

    if "law_of_sines" in name or "sine_law" in name:
        return "law_of_sines"

    if "law_of_cosines" in name or "cosine_law" in name:
        return "law_of_cosines"

    if "triangle" in name:
        return "triangle_trigonometry"

    if "polar" in name:
        return "polar_coordinates"

    if "vector" in name:
        return "vector_trigonometry"

    if "bearing" in name:
        return "bearings"

    return "trigonometry_utilities"


def _function_parameters(function):
    """
    Generate metadata directly from a Python function signature.
    """

    signature = inspect.signature(function)

    parameters = {}

    for parameter_name, parameter in signature.parameters.items():

        required = (
            parameter.default
            is inspect.Parameter.empty
        )

        if parameter.annotation is inspect.Parameter.empty:
            parameter_type = "value"
        else:
            parameter_type = str(
                parameter.annotation
            )

        parameter_data = {
            "type": parameter_type,
            "required": required,
            "description": (
                f"Input parameter '{parameter_name}'."
            )
        }

        if not required:
            parameter_data["default"] = parameter.default

        parameters[parameter_name] = parameter_data

    return parameters


def _function_description(function):
    """
    Generate a description for a registered math function.
    """

    docstring = inspect.getdoc(function)

    if docstring:
        return docstring.split("\n")[0]

    readable_name = function.__name__.replace(
        "_",
        " "
    )

    return (
        f"Perform the math operation: "
        f"{readable_name}."
    )


def _function_keywords(function):
    """
    Generate basic search keywords from a function name.
    """

    function_name = function.__name__

    words = function_name.split("_")

    keywords = [
        function_name,
        function_name.replace("_", " "),
        *words
    ]

    # Remove duplicates while preserving order
    return list(
        dict.fromkeys(keywords)
    )


def register_trigonometry_operations(registry):
    """
    Automatically register all public functions defined
    directly inside math_engine.trigonometry.
    """

    functions = inspect.getmembers(
        trigonometry_module,
        inspect.isfunction
    )

    for function_name, function in functions:

        # Ignore private/internal functions
        if function_name.startswith("_"):
            continue

        # Only register functions actually defined in
        # trigonometry.py. This prevents imported SymPy
        # functions such as sin(), cos(), etc. from appearing
        # in the NOVA registry.
        if (
            function.__module__
            != trigonometry_module.__name__
        ):
            continue

        registry.register(
            name=function_name,
            function=function,
            subsystem="trigonometry",
            description=_function_description(
                function
            ),
            parameters=_function_parameters(
                function
            ),
            returns={
                "type": "expression",
                "description": (
                    "Result returned by the "
                    "trigonometry operation."
                )
            },
            keywords=_function_keywords(
                function
            ),
            category=_trig_category(
                function_name
            )
        )


# ============================================================
# CALCULUS REGISTRATION
# ============================================================

def _calculus_category(function_name):
    """
    Infer a Calculus category from a function name.
    """

    name = function_name.lower()

    if "limit" in name:
        return "limits"

    if "continu" in name or "discontinu" in name:
        return "continuity"

    if (
        "derivative" in name
        or "differenti" in name
        or "tangent_line" in name
        or "normal_line" in name
    ):
        return "derivatives"

    if (
        "critical_point" in name
        or "inflection" in name
        or "extrema" in name
        or "optimization" in name
        or "second_derivative_test" in name
    ):
        return "derivative_applications"

    if "related_rate" in name:
        return "related_rates"

    if (
        "linearization" in name
        or "differential" in name
        or "error" in name
    ):
        return "linearization_differentials"

    if (
        "antiderivative" in name
        or "indefinite_integral" in name
    ):
        return "antiderivatives"

    if (
        "riemann" in name
        or "trapezoidal" in name
        or "simpson" in name
    ):
        return "numerical_integration"

    if "improper_integral" in name:
        return "improper_integrals"

    if (
        "double_integral" in name
        or "triple_integral" in name
        or "multiple_integral" in name
    ):
        return "multiple_integrals"

    if (
        "polar_double_integral" in name
        or "cylindrical_jacobian" in name
        or "spherical_jacobian" in name
    ):
        return "coordinate_integration"

    if (
        "integral" in name
        or "average_function_value" in name
        or "signed_area" in name
    ):
        return "integration"

    if (
        "area_under_curve" in name
        or "area_between_curves" in name
        or "curve_intersections" in name
    ):
        return "area_applications"

    if (
        "volume" in name
        or "disk_" in name
        or "washer_" in name
        or "shell_" in name
    ):
        return "volume_applications"

    if (
        "arc_length" in name
        or "surface_area" in name
    ):
        return "arc_length_surface_area"

    if "sequence" in name:
        return "sequences"

    if (
        "power_series" in name
        or "taylor" in name
        or "maclaurin" in name
    ):
        return "power_taylor_series"

    if (
        "series" in name
        or "partial_sum" in name
        or "nth_term_test" in name
    ):
        return "infinite_series"

    if "parametric" in name:
        return "parametric_calculus"

    if "polar" in name:
        return "polar_calculus"

    if (
        "partial_derivative" in name
        or "mixed_partial" in name
    ):
        return "partial_derivatives"

    if (
        "gradient" in name
        or "directional_derivative" in name
        or "tangent_plane" in name
    ):
        return "gradient_directional_derivatives"

    if (
        "multivariable_critical" in name
        or "hessian" in name
        or "lagrange" in name
    ):
        return "multivariable_optimization"

    if "multivariable" in name or "level_curve" in name:
        return "multivariable_functions"

    if (
        "vector_" in name
        or "velocity_vector" in name
        or "acceleration_vector" in name
    ):
        return "vector_calculus"

    if (
        "line_integral" in name
        or "surface_integral" in name
    ):
        return "line_surface_integrals"

    if (
        "conservative" in name
        or "fundamental_line_integral" in name
    ):
        return "vector_calculus_theorems"

    return "calculus_utilities"


def register_calculus_operations(registry):
    """
    Automatically register all public functions defined
    directly inside math_engine.calculus.
    """

    functions = inspect.getmembers(
        calculus_module,
        inspect.isfunction
    )

    for function_name, function in functions:

        if function_name.startswith("_"):
            continue

        if (
            function.__module__
            != calculus_module.__name__
        ):
            continue

        operation_name = function_name

        # If another subsystem already uses this name,
        # namespace the Calculus version.
        if registry.exists(operation_name):
            operation_name = f"calculus_{function_name}"

        registry.register(
            name=operation_name,
            function=function,
            subsystem="calculus",
            description=_function_description(
                function
            ),
            parameters=_function_parameters(
                function
            ),
            returns={
                "type": "expression",
                "description": (
                    "Result returned by the "
                    "calculus operation."
                )
            },
            keywords=_function_keywords(
                function
            ),
            category=_calculus_category(
                function_name
            )
        )


# ============================================================
# GLOBAL MATH REGISTRY
# ============================================================

math_registry = MathRegistry()


# ============================================================
# REGISTER SUBSYSTEMS
# ============================================================

register_arithmetic_operations(
    math_registry
)

register_algebra_operations(
    math_registry
)

register_geometry_operations(
    math_registry
)

register_trigonometry_operations(
    math_registry
)

register_calculus_operations(
    math_registry
)