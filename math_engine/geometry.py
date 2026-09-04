"""
N.O.V.A. Geometry Subsystem

Provides geometric calculations for the N.O.V.A. math engine.

This subsystem uses SymPy so geometric calculations can preserve
exact mathematical values such as pi, fractions, and radicals
whenever possible.
"""

from sympy import (
    sympify,
    pi,
    sqrt,
    Abs,
    simplify
)


# ============================================================
# VALUE PARSING
# ============================================================

def parse_value(value):
    """
    Convert an input value into a SymPy expression.

    Examples:
        parse_value(5)
        -> 5

        parse_value("sqrt(2)")
        -> sqrt(2)
    """

    return sympify(value)


# ============================================================
# RECTANGLE
# ============================================================

def rectangle_area(length, width):
    """
    Calculate the area of a rectangle.

    Formula:
        A = length * width
    """

    length = parse_value(length)
    width = parse_value(width)

    return length * width


def rectangle_perimeter(length, width):
    """
    Calculate the perimeter of a rectangle.

    Formula:
        P = 2(length + width)
    """

    length = parse_value(length)
    width = parse_value(width)

    return 2 * (length + width)


# ============================================================
# SQUARE
# ============================================================

def square_area(side):
    """
    Calculate the area of a square.

    Formula:
        A = side^2
    """

    side = parse_value(side)

    return side**2


def square_perimeter(side):
    """
    Calculate the perimeter of a square.

    Formula:
        P = 4 * side
    """

    side = parse_value(side)

    return 4 * side


# ============================================================
# TRIANGLE
# ============================================================

def triangle_area(base, height):
    """
    Calculate the area of a triangle.

    Formula:
        A = (1/2) * base * height
    """

    base = parse_value(base)
    height = parse_value(height)

    return base * height / 2


def triangle_perimeter(side_a, side_b, side_c):
    """
    Calculate the perimeter of a triangle.
    """

    side_a = parse_value(side_a)
    side_b = parse_value(side_b)
    side_c = parse_value(side_c)

    return side_a + side_b + side_c


# ============================================================
# CIRCLE
# ============================================================

def circle_area(radius):
    """
    Calculate the area of a circle.

    Formula:
        A = pi * r^2
    """

    radius = parse_value(radius)

    return pi * radius**2


def circle_circumference(radius):
    """
    Calculate the circumference of a circle.

    Formula:
        C = 2 * pi * r
    """

    radius = parse_value(radius)

    return 2 * pi * radius


# ============================================================
# PARALLELOGRAM
# ============================================================

def parallelogram_area(base, height):
    """
    Calculate the area of a parallelogram.

    Formula:
        A = base * height
    """

    base = parse_value(base)
    height = parse_value(height)

    return base * height


# ============================================================
# TRAPEZOID
# ============================================================

def trapezoid_area(base_1, base_2, height):
    """
    Calculate the area of a trapezoid.

    Formula:
        A = (1/2)(base_1 + base_2) * height
    """

    base_1 = parse_value(base_1)
    base_2 = parse_value(base_2)
    height = parse_value(height)

    return (base_1 + base_2) * height / 2


# ============================================================
# RHOMBUS
# ============================================================

def rhombus_area(diagonal_1, diagonal_2):
    """
    Calculate the area of a rhombus using its diagonals.

    Formula:
        A = (1/2) * d1 * d2
    """

    diagonal_1 = parse_value(diagonal_1)
    diagonal_2 = parse_value(diagonal_2)

    return diagonal_1 * diagonal_2 / 2


# ============================================================
# COORDINATE GEOMETRY
# ============================================================

def distance_between_points(x1, y1, x2, y2):
    """
    Calculate the distance between two points.

    Points:
        (x1, y1)
        (x2, y2)
    """

    x1 = parse_value(x1)
    y1 = parse_value(y1)
    x2 = parse_value(x2)
    y2 = parse_value(y2)

    return sqrt(
        (x2 - x1)**2 +
        (y2 - y1)**2
    )


def midpoint(x1, y1, x2, y2):
    """
    Calculate the midpoint between two points.

    Returns:
        (x_midpoint, y_midpoint)
    """

    x1 = parse_value(x1)
    y1 = parse_value(y1)
    x2 = parse_value(x2)
    y2 = parse_value(y2)

    x_midpoint = (x1 + x2) / 2
    y_midpoint = (y1 + y2) / 2

    return (
        x_midpoint,
        y_midpoint
    )


def slope(x1, y1, x2, y2):
    """
    Calculate the slope between two points.

    Formula:
        m = (y2 - y1) / (x2 - x1)
    """

    x1 = parse_value(x1)
    y1 = parse_value(y1)
    x2 = parse_value(x2)
    y2 = parse_value(y2)

    if x2 == x1:
        raise ValueError(
            "Slope is undefined for a vertical line."
        )

    return (y2 - y1) / (x2 - x1)


def line_from_point_slope(x1, y1, line_slope):
    """
    Return the slope-intercept form of a line.

    Uses:
        y = mx + b

    Given:
        point (x1, y1)
        slope m

    Returns:
        (m, b)
    """

    x1 = parse_value(x1)
    y1 = parse_value(y1)
    line_slope = parse_value(line_slope)

    intercept = y1 - line_slope * x1

    return (
        line_slope,
        intercept
    )


def line_from_two_points(x1, y1, x2, y2):
    """
    Find the slope-intercept form of a line
    passing through two points.

    Returns:
        (slope, y_intercept)
    """

    line_slope = slope(
        x1,
        y1,
        x2,
        y2
    )

    return line_from_point_slope(
        x1,
        y1,
        line_slope
    )


def are_parallel(slope_1, slope_2):
    """
    Determine whether two lines are parallel.

    Parallel lines have equal slopes.
    """

    slope_1 = parse_value(slope_1)
    slope_2 = parse_value(slope_2)

    return simplify(
        slope_1 - slope_2
    ) == 0


def are_perpendicular(slope_1, slope_2):
    """
    Determine whether two non-vertical lines
    are perpendicular.

    Perpendicular slopes satisfy:
        m1 * m2 = -1
    """

    slope_1 = parse_value(slope_1)
    slope_2 = parse_value(slope_2)

    return simplify(
        slope_1 * slope_2 + 1
    ) == 0


# ============================================================
# TRIANGLE GEOMETRY
# ============================================================

def pythagorean_hypotenuse(side_a, side_b):
    """
    Calculate the hypotenuse of a right triangle.

    Formula:
        c = sqrt(a^2 + b^2)
    """

    side_a = parse_value(side_a)
    side_b = parse_value(side_b)

    return simplify(
        sqrt(side_a**2 + side_b**2)
    )


def pythagorean_leg(hypotenuse, known_leg):
    """
    Calculate a missing leg of a right triangle.

    Formula:
        a = sqrt(c^2 - b^2)
    """

    hypotenuse = parse_value(hypotenuse)
    known_leg = parse_value(known_leg)

    if hypotenuse <= 0 or known_leg <= 0:
        raise ValueError(
            "Triangle side lengths must be positive."
        )

    if known_leg >= hypotenuse:
        raise ValueError(
            "The hypotenuse must be longer than either leg."
        )

    return simplify(
        sqrt(
            hypotenuse**2 -
            known_leg**2
        )
    )


def triangle_is_valid(side_a, side_b, side_c):
    """
    Determine whether three side lengths can form a triangle.

    Triangle inequality:
        a + b > c
        a + c > b
        b + c > a
    """

    side_a = parse_value(side_a)
    side_b = parse_value(side_b)
    side_c = parse_value(side_c)

    if (
        side_a <= 0 or
        side_b <= 0 or
        side_c <= 0
    ):
        return False

    return (
        side_a + side_b > side_c
        and side_a + side_c > side_b
        and side_b + side_c > side_a
    )


def heron_triangle_area(side_a, side_b, side_c):
    """
    Calculate triangle area using Heron's formula.

    Requires all three side lengths.
    """

    side_a = parse_value(side_a)
    side_b = parse_value(side_b)
    side_c = parse_value(side_c)

    if not triangle_is_valid(
        side_a,
        side_b,
        side_c
    ):
        raise ValueError(
            "The provided sides do not form a valid triangle."
        )

    semiperimeter = (
        side_a +
        side_b +
        side_c
    ) / 2

    area = sqrt(
        semiperimeter
        * (semiperimeter - side_a)
        * (semiperimeter - side_b)
        * (semiperimeter - side_c)
    )

    return simplify(area)


def missing_triangle_angle(angle_1, angle_2):
    """
    Find the third interior angle of a triangle.

    Triangle angles sum to 180 degrees.
    """

    angle_1 = parse_value(angle_1)
    angle_2 = parse_value(angle_2)

    angle_3 = 180 - angle_1 - angle_2

    if (
        angle_1 <= 0 or
        angle_2 <= 0 or
        angle_3 <= 0
    ):
        raise ValueError(
            "The provided angles cannot form a valid triangle."
        )

    return simplify(angle_3)


def classify_triangle_by_sides(side_a, side_b, side_c):
    """
    Classify a triangle by its side lengths.

    Returns:
        equilateral
        isosceles
        scalene
    """

    side_a = parse_value(side_a)
    side_b = parse_value(side_b)
    side_c = parse_value(side_c)

    if not triangle_is_valid(
        side_a,
        side_b,
        side_c
    ):
        raise ValueError(
            "The provided sides do not form a valid triangle."
        )

    if side_a == side_b == side_c:
        return "equilateral"

    if (
        side_a == side_b or
        side_a == side_c or
        side_b == side_c
    ):
        return "isosceles"

    return "scalene"


def classify_triangle_by_angles(angle_1, angle_2, angle_3):
    """
    Classify a triangle by its angles.

    Returns:
        acute
        right
        obtuse
    """

    angle_1 = parse_value(angle_1)
    angle_2 = parse_value(angle_2)
    angle_3 = parse_value(angle_3)

    if (
        angle_1 <= 0 or
        angle_2 <= 0 or
        angle_3 <= 0 or
        simplify(
            angle_1 +
            angle_2 +
            angle_3
        ) != 180
    ):
        raise ValueError(
            "The provided angles do not form a valid triangle."
        )

    angles = [
        angle_1,
        angle_2,
        angle_3
    ]

    if 90 in angles:
        return "right"

    if any(
        angle > 90
        for angle in angles
    ):
        return "obtuse"

    return "acute"


# ============================================================
# CIRCLES AND REGULAR POLYGONS
# ============================================================

def circle_diameter(radius):
    """
    Calculate the diameter of a circle.

    Formula:
        d = 2r
    """

    radius = parse_value(radius)

    if radius < 0:
        raise ValueError(
            "Radius cannot be negative."
        )

    return 2 * radius


def arc_length(radius, central_angle_degrees):
    """
    Calculate arc length using an angle in degrees.

    Formula:
        L = (theta / 360) * 2*pi*r
    """

    radius = parse_value(radius)
    angle = parse_value(central_angle_degrees)

    if radius < 0:
        raise ValueError(
            "Radius cannot be negative."
        )

    return simplify(
        (angle / 360) *
        2 * pi * radius
    )


def sector_area(radius, central_angle_degrees):
    """
    Calculate the area of a circular sector.

    Formula:
        A = (theta / 360) * pi*r^2
    """

    radius = parse_value(radius)
    angle = parse_value(central_angle_degrees)

    if radius < 0:
        raise ValueError(
            "Radius cannot be negative."
        )

    return simplify(
        (angle / 360) *
        pi * radius**2
    )


def semicircle_area(radius):
    """
    Calculate the area of a semicircle.
    """

    radius = parse_value(radius)

    if radius < 0:
        raise ValueError(
            "Radius cannot be negative."
        )

    return simplify(
        pi * radius**2 / 2
    )


def annulus_area(outer_radius, inner_radius):
    """
    Calculate the area of an annulus.

    Formula:
        A = pi(R^2 - r^2)
    """

    outer_radius = parse_value(outer_radius)
    inner_radius = parse_value(inner_radius)

    if outer_radius < 0 or inner_radius < 0:
        raise ValueError(
            "Radii cannot be negative."
        )

    if inner_radius > outer_radius:
        raise ValueError(
            "Inner radius cannot exceed outer radius."
        )

    return simplify(
        pi * (
            outer_radius**2 -
            inner_radius**2
        )
    )


def regular_polygon_perimeter(number_of_sides, side_length):
    """
    Calculate the perimeter of a regular polygon.

    Formula:
        P = n*s
    """

    number_of_sides = parse_value(number_of_sides)
    side_length = parse_value(side_length)

    if (
        number_of_sides.is_integer is not True
        or number_of_sides < 3
    ):
        raise ValueError(
            "A polygon must have at least 3 sides."
        )

    if side_length <= 0:
        raise ValueError(
            "Side length must be positive."
        )

    return simplify(
        number_of_sides *
        side_length
    )


def regular_polygon_interior_angle(number_of_sides):
    """
    Calculate one interior angle of a regular polygon.

    Formula:
        angle = ((n - 2) * 180) / n
    """

    number_of_sides = parse_value(
        number_of_sides
    )

    if (
        number_of_sides.is_integer is not True
        or number_of_sides < 3
    ):
        raise ValueError(
            "A polygon must have at least 3 sides."
        )

    return simplify(
        (
            (number_of_sides - 2) * 180
        ) / number_of_sides
    )


def polygon_interior_angle_sum(number_of_sides):
    """
    Calculate the sum of the interior angles
    of a polygon.

    Formula:
        S = (n - 2) * 180
    """

    number_of_sides = parse_value(
        number_of_sides
    )

    if (
        number_of_sides.is_integer is not True
        or number_of_sides < 3
    ):
        raise ValueError(
            "A polygon must have at least 3 sides."
        )

    return (
        number_of_sides - 2
    ) * 180


def regular_polygon_area_from_apothem(
    number_of_sides,
    side_length,
    apothem
):
    """
    Calculate the area of a regular polygon
    using its perimeter and apothem.

    Formula:
        A = (1/2) * P * a
    """

    number_of_sides = parse_value(
        number_of_sides
    )

    side_length = parse_value(
        side_length
    )

    apothem = parse_value(
        apothem
    )

    perimeter = regular_polygon_perimeter(
        number_of_sides,
        side_length
    )

    if apothem <= 0:
        raise ValueError(
            "Apothem must be positive."
        )

    return simplify(
        perimeter *
        apothem / 2
    )

# ============================================================
# 3D GEOMETRY / SOLID GEOMETRY
# ============================================================

def cube_volume(side):
    """
    Calculate the volume of a cube.

    Formula:
        V = s^3
    """

    side = parse_value(side)

    if side <= 0:
        raise ValueError(
            "Side length must be positive."
        )

    return simplify(side**3)


def cube_surface_area(side):
    """
    Calculate the surface area of a cube.

    Formula:
        SA = 6s^2
    """

    side = parse_value(side)

    if side <= 0:
        raise ValueError(
            "Side length must be positive."
        )

    return simplify(6 * side**2)


def rectangular_prism_volume(length, width, height):
    """
    Calculate the volume of a rectangular prism.

    Formula:
        V = lwh
    """

    length = parse_value(length)
    width = parse_value(width)
    height = parse_value(height)

    if length <= 0 or width <= 0 or height <= 0:
        raise ValueError(
            "All dimensions must be positive."
        )

    return simplify(
        length * width * height
    )


def rectangular_prism_surface_area(length, width, height):
    """
    Calculate the surface area of a rectangular prism.

    Formula:
        SA = 2(lw + lh + wh)
    """

    length = parse_value(length)
    width = parse_value(width)
    height = parse_value(height)

    if length <= 0 or width <= 0 or height <= 0:
        raise ValueError(
            "All dimensions must be positive."
        )

    return simplify(
        2 * (
            length * width +
            length * height +
            width * height
        )
    )


def cylinder_volume(radius, height):
    """
    Calculate the volume of a cylinder.

    Formula:
        V = pi*r^2*h
    """

    radius = parse_value(radius)
    height = parse_value(height)

    if radius <= 0 or height <= 0:
        raise ValueError(
            "Radius and height must be positive."
        )

    return simplify(
        pi * radius**2 * height
    )


def cylinder_surface_area(radius, height):
    """
    Calculate the total surface area of a cylinder.

    Formula:
        SA = 2*pi*r^2 + 2*pi*r*h
    """

    radius = parse_value(radius)
    height = parse_value(height)

    if radius <= 0 or height <= 0:
        raise ValueError(
            "Radius and height must be positive."
        )

    return simplify(
        2 * pi * radius**2 +
        2 * pi * radius * height
    )


def cone_volume(radius, height):
    """
    Calculate the volume of a cone.

    Formula:
        V = (1/3)*pi*r^2*h
    """

    radius = parse_value(radius)
    height = parse_value(height)

    if radius <= 0 or height <= 0:
        raise ValueError(
            "Radius and height must be positive."
        )

    return simplify(
        pi * radius**2 * height / 3
    )


def cone_surface_area(radius, height):
    """
    Calculate the total surface area of a right cone.

    The slant height is calculated automatically.

    Formula:
        l = sqrt(r^2 + h^2)
        SA = pi*r^2 + pi*r*l
    """

    radius = parse_value(radius)
    height = parse_value(height)

    if radius <= 0 or height <= 0:
        raise ValueError(
            "Radius and height must be positive."
        )

    slant_height = sqrt(
        radius**2 + height**2
    )

    return simplify(
        pi * radius**2 +
        pi * radius * slant_height
    )


def sphere_volume(radius):
    """
    Calculate the volume of a sphere.

    Formula:
        V = (4/3)*pi*r^3
    """

    radius = parse_value(radius)

    if radius <= 0:
        raise ValueError(
            "Radius must be positive."
        )

    return simplify(
        4 * pi * radius**3 / 3
    )


def sphere_surface_area(radius):
    """
    Calculate the surface area of a sphere.

    Formula:
        SA = 4*pi*r^2
    """

    radius = parse_value(radius)

    if radius <= 0:
        raise ValueError(
            "Radius must be positive."
        )

    return simplify(
        4 * pi * radius**2
    )


def hemisphere_volume(radius):
    """
    Calculate the volume of a hemisphere.

    Formula:
        V = (2/3)*pi*r^3
    """

    radius = parse_value(radius)

    if radius <= 0:
        raise ValueError(
            "Radius must be positive."
        )

    return simplify(
        2 * pi * radius**3 / 3
    )


def hemisphere_surface_area(radius):
    """
    Calculate the total surface area of a hemisphere,
    including the circular base.

    Formula:
        SA = 3*pi*r^2
    """

    radius = parse_value(radius)

    if radius <= 0:
        raise ValueError(
            "Radius must be positive."
        )

    return simplify(
        3 * pi * radius**2
    )


def square_pyramid_volume(base_side, height):
    """
    Calculate the volume of a square pyramid.

    Formula:
        V = (1/3)*s^2*h
    """

    base_side = parse_value(base_side)
    height = parse_value(height)

    if base_side <= 0 or height <= 0:
        raise ValueError(
            "Base side and height must be positive."
        )

    return simplify(
        base_side**2 * height / 3
    )


def square_pyramid_surface_area(base_side, slant_height):
    """
    Calculate the total surface area of a square pyramid.

    Formula:
        SA = s^2 + 2sl
    """

    base_side = parse_value(base_side)
    slant_height = parse_value(slant_height)

    if base_side <= 0 or slant_height <= 0:
        raise ValueError(
            "Base side and slant height must be positive."
        )

    return simplify(
        base_side**2 +
        2 * base_side * slant_height
    )


def prism_volume(base_area, height):
    """
    Calculate the volume of a general prism.

    Formula:
        V = B*h
    """

    base_area = parse_value(base_area)
    height = parse_value(height)

    if base_area <= 0 or height <= 0:
        raise ValueError(
            "Base area and height must be positive."
        )

    return simplify(
        base_area * height
    )


# ============================================================
# LINE GEOMETRY
# ============================================================

def line_equation_slope_intercept(slope_value, y_intercept):
    """
    Return the symbolic slope-intercept equation:

        y = mx + b

    Returns:
        SymPy equation
    """

    from sympy import Eq, symbols

    x, y = symbols("x y")

    slope_value = parse_value(slope_value)
    y_intercept = parse_value(y_intercept)

    return Eq(
        y,
        slope_value * x + y_intercept
    )


def line_equation_point_slope(
    x1,
    y1,
    slope_value
):
    """
    Return the point-slope equation:

        y - y1 = m(x - x1)
    """

    from sympy import Eq, symbols

    x, y = symbols("x y")

    x1 = parse_value(x1)
    y1 = parse_value(y1)
    slope_value = parse_value(slope_value)

    return Eq(
        y - y1,
        slope_value * (x - x1)
    )


def line_standard_form_from_points(
    x1,
    y1,
    x2,
    y2
):
    """
    Return standard form coefficients:

        Ax + By = C

    Returns:
        (A, B, C)
    """

    x1 = parse_value(x1)
    y1 = parse_value(y1)
    x2 = parse_value(x2)
    y2 = parse_value(y2)

    if x1 == x2 and y1 == y2:
        raise ValueError(
            "Two distinct points are required."
        )

    A = simplify(y2 - y1)
    B = simplify(x1 - x2)
    C = simplify(
        A * x1 +
        B * y1
    )

    return (
        A,
        B,
        C
    )


def line_x_intercept(slope_value, y_intercept):
    """
    Find the x-intercept of:

        y = mx + b
    """

    slope_value = parse_value(slope_value)
    y_intercept = parse_value(y_intercept)

    if slope_value == 0:
        if y_intercept == 0:
            return "all real x"
        return None

    return simplify(
        -y_intercept /
        slope_value
    )


def line_y_intercept(slope_value, y_intercept):
    """
    Return the y-intercept of:

        y = mx + b
    """

    slope_value = parse_value(slope_value)
    y_intercept = parse_value(y_intercept)

    return y_intercept


def line_intersection(
    slope_1,
    intercept_1,
    slope_2,
    intercept_2
):
    """
    Find the intersection point of two
    non-vertical lines:

        y = m1*x + b1
        y = m2*x + b2

    Returns:
        (x, y)

    Returns None for parallel distinct lines.
    """

    slope_1 = parse_value(slope_1)
    intercept_1 = parse_value(intercept_1)
    slope_2 = parse_value(slope_2)
    intercept_2 = parse_value(intercept_2)

    if simplify(
        slope_1 - slope_2
    ) == 0:

        if simplify(
            intercept_1 - intercept_2
        ) == 0:
            return "same line"

        return None

    x_value = simplify(
        (intercept_2 - intercept_1) /
        (slope_1 - slope_2)
    )

    y_value = simplify(
        slope_1 * x_value +
        intercept_1
    )

    return (
        x_value,
        y_value
    )


def point_to_line_distance(
    point_x,
    point_y,
    A,
    B,
    C
):
    """
    Distance from a point to a line.

    Line:
        Ax + By + C = 0

    Formula:
        d = |Ax0 + By0 + C| / sqrt(A^2 + B^2)
    """

    point_x = parse_value(point_x)
    point_y = parse_value(point_y)
    A = parse_value(A)
    B = parse_value(B)
    C = parse_value(C)

    if A == 0 and B == 0:
        raise ValueError(
            "A and B cannot both be zero."
        )

    return simplify(
        Abs(
            A * point_x +
            B * point_y +
            C
        ) /
        sqrt(
            A**2 +
            B**2
        )
    )


def perpendicular_slope(slope_value):
    """
    Find the slope of a line perpendicular
    to a non-horizontal, non-vertical line.

    Formula:
        m_perpendicular = -1/m
    """

    slope_value = parse_value(slope_value)

    if slope_value == 0:
        return "undefined"

    return simplify(
        -1 / slope_value
    )


def perpendicular_bisector(
    x1,
    y1,
    x2,
    y2
):
    """
    Find the perpendicular bisector of
    the segment between two points.

    Returns:
        dictionary describing the line
    """

    x1 = parse_value(x1)
    y1 = parse_value(y1)
    x2 = parse_value(x2)
    y2 = parse_value(y2)

    if x1 == x2 and y1 == y2:
        raise ValueError(
            "Two distinct points are required."
        )

    mid_x, mid_y = midpoint(
        x1,
        y1,
        x2,
        y2
    )

    if x1 == x2:
        return {
            "type": "horizontal",
            "y": mid_y
        }

    if y1 == y2:
        return {
            "type": "vertical",
            "x": mid_x
        }

    original_slope = slope(
        x1,
        y1,
        x2,
        y2
    )

    bisector_slope = simplify(
        -1 / original_slope
    )

    intercept = simplify(
        mid_y -
        bisector_slope * mid_x
    )

    return {
        "type": "slope-intercept",
        "slope": bisector_slope,
        "intercept": intercept
    }


# ============================================================
# ADVANCED TRIANGLE GEOMETRY
# ============================================================

def triangle_angle_sum_is_valid(
    angle_1,
    angle_2,
    angle_3
):
    """
    Check whether three angles form a valid triangle.
    """

    angle_1 = parse_value(angle_1)
    angle_2 = parse_value(angle_2)
    angle_3 = parse_value(angle_3)

    if (
        angle_1 <= 0 or
        angle_2 <= 0 or
        angle_3 <= 0
    ):
        return False

    return simplify(
        angle_1 +
        angle_2 +
        angle_3
    ) == 180


def triangle_exterior_angle(
    remote_angle_1,
    remote_angle_2
):
    """
    Calculate an exterior angle using
    the two remote interior angles.

    Formula:
        exterior = angle1 + angle2
    """

    remote_angle_1 = parse_value(
        remote_angle_1
    )

    remote_angle_2 = parse_value(
        remote_angle_2
    )

    if (
        remote_angle_1 <= 0 or
        remote_angle_2 <= 0
    ):
        raise ValueError(
            "Angles must be positive."
        )

    result = simplify(
        remote_angle_1 +
        remote_angle_2
    )

    if result >= 180:
        raise ValueError(
            "The resulting exterior angle must be less than 180 degrees."
        )

    return result


def classify_triangle_by_side_lengths(
    side_a,
    side_b,
    side_c
):
    """
    Classify a triangle as acute, right,
    or obtuse using side lengths.
    """

    side_a = parse_value(side_a)
    side_b = parse_value(side_b)
    side_c = parse_value(side_c)

    if not triangle_is_valid(
        side_a,
        side_b,
        side_c
    ):
        raise ValueError(
            "The provided sides do not form a valid triangle."
        )

    sides = sorted(
        [side_a, side_b, side_c],
        key=lambda value: float(value)
    )

    a, b, c = sides

    comparison = simplify(
        a**2 +
        b**2 -
        c**2
    )

    if comparison == 0:
        return "right"

    if comparison > 0:
        return "acute"

    return "obtuse"


def equilateral_triangle_height(side):
    """
    Calculate the height of an equilateral triangle.

    Formula:
        h = sqrt(3)/2 * s
    """

    side = parse_value(side)

    if side <= 0:
        raise ValueError(
            "Side length must be positive."
        )

    return simplify(
        sqrt(3) *
        side / 2
    )


def equilateral_triangle_area(side):
    """
    Calculate the area of an equilateral triangle.

    Formula:
        A = sqrt(3)/4 * s^2
    """

    side = parse_value(side)

    if side <= 0:
        raise ValueError(
            "Side length must be positive."
        )

    return simplify(
        sqrt(3) *
        side**2 / 4
    )


def isosceles_triangle_height(
    equal_side,
    base
):
    """
    Calculate the height of an isosceles triangle.

    Formula:
        h = sqrt(a^2 - (b/2)^2)
    """

    equal_side = parse_value(equal_side)
    base = parse_value(base)

    if (
        equal_side <= 0 or
        base <= 0
    ):
        raise ValueError(
            "Side lengths must be positive."
        )

    if base >= 2 * equal_side:
        raise ValueError(
            "The provided sides do not form an isosceles triangle."
        )

    return simplify(
        sqrt(
            equal_side**2 -
            (base / 2)**2
        )
    )


def isosceles_triangle_area(
    equal_side,
    base
):
    """
    Calculate the area of an isosceles triangle.
    """

    height = isosceles_triangle_height(
        equal_side,
        base
    )

    return simplify(
        base * height / 2
    )


def triangle_centroid(
    x1,
    y1,
    x2,
    y2,
    x3,
    y3
):
    """
    Calculate the centroid of a triangle.

    Returns:
        (x, y)
    """

    x1 = parse_value(x1)
    y1 = parse_value(y1)
    x2 = parse_value(x2)
    y2 = parse_value(y2)
    x3 = parse_value(x3)
    y3 = parse_value(y3)

    return (
        simplify(
            (x1 + x2 + x3) / 3
        ),
        simplify(
            (y1 + y2 + y3) / 3
        )
    )


def triangle_inradius_from_area(
    area,
    side_a,
    side_b,
    side_c
):
    """
    Calculate the inradius.

    Formula:
        r = A / s
    """

    area = parse_value(area)
    side_a = parse_value(side_a)
    side_b = parse_value(side_b)
    side_c = parse_value(side_c)

    if not triangle_is_valid(
        side_a,
        side_b,
        side_c
    ):
        raise ValueError(
            "The provided sides do not form a valid triangle."
        )

    semiperimeter = (
        side_a +
        side_b +
        side_c
    ) / 2

    return simplify(
        area /
        semiperimeter
    )


def triangle_circumradius(
    side_a,
    side_b,
    side_c
):
    """
    Calculate circumradius from three sides.

    Formula:
        R = abc / (4A)
    """

    side_a = parse_value(side_a)
    side_b = parse_value(side_b)
    side_c = parse_value(side_c)

    area = heron_triangle_area(
        side_a,
        side_b,
        side_c
    )

    return simplify(
        side_a *
        side_b *
        side_c /
        (4 * area)
    )


# ============================================================
# ADVANCED CIRCLE GEOMETRY
# ============================================================

def circle_radius_from_diameter(diameter):
    """
    Calculate radius from diameter.
    """

    diameter = parse_value(diameter)

    if diameter < 0:
        raise ValueError(
            "Diameter cannot be negative."
        )

    return simplify(
        diameter / 2
    )


def circle_radius_from_circumference(
    circumference
):
    """
    Calculate radius from circumference.

    Formula:
        r = C / (2*pi)
    """

    circumference = parse_value(
        circumference
    )

    if circumference < 0:
        raise ValueError(
            "Circumference cannot be negative."
        )

    return simplify(
        circumference /
        (2 * pi)
    )


def circle_radius_from_area(area):
    """
    Calculate radius from area.

    Formula:
        r = sqrt(A/pi)
    """

    area = parse_value(area)

    if area < 0:
        raise ValueError(
            "Area cannot be negative."
        )

    return simplify(
        sqrt(
            area / pi
        )
    )


def circle_circumference_from_diameter(
    diameter
):
    """
    Calculate circumference from diameter.

    Formula:
        C = pi*d
    """

    diameter = parse_value(diameter)

    if diameter < 0:
        raise ValueError(
            "Diameter cannot be negative."
        )

    return simplify(
        pi * diameter
    )


def chord_length(
    radius,
    distance_from_center
):
    """
    Calculate chord length from radius and
    perpendicular distance from center.

    Formula:
        L = 2*sqrt(r^2 - d^2)
    """

    radius = parse_value(radius)

    distance_from_center = parse_value(
        distance_from_center
    )

    if (
        radius <= 0 or
        distance_from_center < 0
    ):
        raise ValueError(
            "Invalid radius or center distance."
        )

    if distance_from_center > radius:
        raise ValueError(
            "Distance from center cannot exceed radius."
        )

    return simplify(
        2 *
        sqrt(
            radius**2 -
            distance_from_center**2
        )
    )


def center_to_chord_distance(
    radius,
    chord
):
    """
    Calculate the perpendicular distance
    from a circle's center to a chord.

    Formula:
        d = sqrt(r^2 - (L/2)^2)
    """

    radius = parse_value(radius)
    chord = parse_value(chord)

    if (
        radius <= 0 or
        chord <= 0
    ):
        raise ValueError(
            "Radius and chord length must be positive."
        )

    if chord > 2 * radius:
        raise ValueError(
            "Chord length cannot exceed the diameter."
        )

    return simplify(
        sqrt(
            radius**2 -
            (chord / 2)**2
        )
    )


def circle_equation(
    center_x,
    center_y,
    radius
):
    """
    Return the standard circle equation:

        (x-h)^2 + (y-k)^2 = r^2
    """

    from sympy import Eq, symbols

    x, y = symbols("x y")

    center_x = parse_value(center_x)
    center_y = parse_value(center_y)
    radius = parse_value(radius)

    if radius <= 0:
        raise ValueError(
            "Radius must be positive."
        )

    return Eq(
        (x - center_x)**2 +
        (y - center_y)**2,
        radius**2
    )


def circle_center_radius_from_standard(
    h,
    k,
    radius_squared
):
    """
    Interpret standard circle parameters:

        (x-h)^2 + (y-k)^2 = r^2

    Returns:
        center, radius
    """

    h = parse_value(h)
    k = parse_value(k)
    radius_squared = parse_value(
        radius_squared
    )

    if radius_squared < 0:
        raise ValueError(
            "Radius squared cannot be negative."
        )

    return {
        "center": (
            h,
            k
        ),
        "radius": simplify(
            sqrt(radius_squared)
        )
    }


# ============================================================
# POLYGON GEOMETRY
# ============================================================

def regular_polygon_exterior_angle(
    number_of_sides
):
    """
    Calculate one exterior angle of a
    regular polygon.

    Formula:
        angle = 360 / n
    """

    number_of_sides = parse_value(
        number_of_sides
    )

    if (
        number_of_sides.is_integer is not True
        or number_of_sides < 3
    ):
        raise ValueError(
            "A polygon must have at least 3 integer sides."
        )

    return simplify(
        360 /
        number_of_sides
    )


def polygon_exterior_angle_sum():
    """
    The sum of the exterior angles
    of any simple polygon is 360 degrees.
    """

    return 360


def polygon_diagonals(
    number_of_sides
):
    """
    Calculate the number of diagonals
    in a polygon.

    Formula:
        D = n(n-3)/2
    """

    number_of_sides = parse_value(
        number_of_sides
    )

    if (
        number_of_sides.is_integer is not True
        or number_of_sides < 3
    ):
        raise ValueError(
            "A polygon must have at least 3 integer sides."
        )

    return simplify(
        number_of_sides *
        (number_of_sides - 3) /
        2
    )


def regular_polygon_apothem(
    number_of_sides,
    side_length
):
    """
    Calculate the apothem of a regular polygon.

    Formula:
        a = s / (2*tan(pi/n))
    """

    from sympy import tan

    number_of_sides = parse_value(
        number_of_sides
    )

    side_length = parse_value(
        side_length
    )

    if (
        number_of_sides.is_integer is not True
        or number_of_sides < 3
    ):
        raise ValueError(
            "A polygon must have at least 3 integer sides."
        )

    if side_length <= 0:
        raise ValueError(
            "Side length must be positive."
        )

    return simplify(
        side_length /
        (
            2 *
            tan(
                pi /
                number_of_sides
            )
        )
    )


def regular_polygon_area(
    number_of_sides,
    side_length
):
    """
    Calculate the area of a regular polygon
    directly from side length.
    """

    perimeter = regular_polygon_perimeter(
        number_of_sides,
        side_length
    )

    apothem = regular_polygon_apothem(
        number_of_sides,
        side_length
    )

    return simplify(
        perimeter *
        apothem / 2
    )


def regular_polygon_side_from_apothem(
    number_of_sides,
    apothem
):
    """
    Calculate side length from apothem.

    Formula:
        s = 2a*tan(pi/n)
    """

    from sympy import tan

    number_of_sides = parse_value(
        number_of_sides
    )

    apothem = parse_value(apothem)

    if (
        number_of_sides.is_integer is not True
        or number_of_sides < 3
    ):
        raise ValueError(
            "A polygon must have at least 3 integer sides."
        )

    if apothem <= 0:
        raise ValueError(
            "Apothem must be positive."
        )

    return simplify(
        2 *
        apothem *
        tan(
            pi /
            number_of_sides
        )
    )


def classify_polygon(
    number_of_sides
):
    """
    Return the common polygon name.
    """

    number_of_sides = parse_value(
        number_of_sides
    )

    if number_of_sides.is_integer is not True:
        raise ValueError(
            "Number of sides must be an integer."
        )

    names = {
        3: "triangle",
        4: "quadrilateral",
        5: "pentagon",
        6: "hexagon",
        7: "heptagon",
        8: "octagon",
        9: "nonagon",
        10: "decagon",
        11: "undecagon",
        12: "dodecagon"
    }

    if number_of_sides < 3:
        raise ValueError(
            "A polygon must have at least 3 sides."
        )

    return names.get(
        int(number_of_sides),
        f"{number_of_sides}-gon"
    )


def polygon_perimeter(side_lengths):
    """
    Calculate perimeter from a sequence
    of side lengths.
    """

    parsed_sides = [
        parse_value(side)
        for side in side_lengths
    ]

    if len(parsed_sides) < 3:
        raise ValueError(
            "A polygon must have at least 3 sides."
        )

    if any(
        side <= 0
        for side in parsed_sides
    ):
        raise ValueError(
            "All side lengths must be positive."
        )

    return simplify(
        sum(parsed_sides)
    )


def shoelace_area(points):
    """
    Calculate the area of a polygon
    from ordered coordinate points.

    points:
        [(x1, y1), (x2, y2), ...]
    """

    if len(points) < 3:
        raise ValueError(
            "At least 3 points are required."
        )

    parsed_points = [
        (
            parse_value(x),
            parse_value(y)
        )
        for x, y in points
    ]

    total_1 = 0
    total_2 = 0

    count = len(parsed_points)

    for index in range(count):
        x1, y1 = parsed_points[index]

        x2, y2 = parsed_points[
            (index + 1) % count
        ]

        total_1 += x1 * y2
        total_2 += y1 * x2

    return simplify(
        Abs(
            total_1 -
            total_2
        ) / 2
    )


# ============================================================
# QUADRILATERAL GEOMETRY
# ============================================================

def rectangle_diagonal(
    length,
    width
):
    """
    Calculate rectangle diagonal.

    Formula:
        d = sqrt(l^2 + w^2)
    """

    length = parse_value(length)
    width = parse_value(width)

    if length <= 0 or width <= 0:
        raise ValueError(
            "Dimensions must be positive."
        )

    return simplify(
        sqrt(
            length**2 +
            width**2
        )
    )


def square_diagonal(side):
    """
    Calculate square diagonal.

    Formula:
        d = s*sqrt(2)
    """

    side = parse_value(side)

    if side <= 0:
        raise ValueError(
            "Side length must be positive."
        )

    return simplify(
        side *
        sqrt(2)
    )


def rhombus_perimeter(side):
    """
    Calculate rhombus perimeter.
    """

    side = parse_value(side)

    if side <= 0:
        raise ValueError(
            "Side length must be positive."
        )

    return simplify(
        4 * side
    )


def parallelogram_perimeter(
    side_a,
    side_b
):
    """
    Calculate parallelogram perimeter.

    Formula:
        P = 2(a+b)
    """

    side_a = parse_value(side_a)
    side_b = parse_value(side_b)

    if side_a <= 0 or side_b <= 0:
        raise ValueError(
            "Side lengths must be positive."
        )

    return simplify(
        2 *
        (
            side_a +
            side_b
        )
    )


def trapezoid_perimeter(
    side_a,
    side_b,
    side_c,
    side_d
):
    """
    Calculate trapezoid perimeter.
    """

    sides = [
        parse_value(side_a),
        parse_value(side_b),
        parse_value(side_c),
        parse_value(side_d)
    ]

    if any(
        side <= 0
        for side in sides
    ):
        raise ValueError(
            "Side lengths must be positive."
        )

    return simplify(
        sum(sides)
    )


def kite_area(
    diagonal_1,
    diagonal_2
):
    """
    Calculate kite area.

    Formula:
        A = d1*d2/2
    """

    diagonal_1 = parse_value(
        diagonal_1
    )

    diagonal_2 = parse_value(
        diagonal_2
    )

    if (
        diagonal_1 <= 0 or
        diagonal_2 <= 0
    ):
        raise ValueError(
            "Diagonals must be positive."
        )

    return simplify(
        diagonal_1 *
        diagonal_2 / 2
    )


def kite_perimeter(
    side_a,
    side_b
):
    """
    Calculate kite perimeter.

    Two pairs of adjacent equal sides:

        P = 2a + 2b
    """

    side_a = parse_value(side_a)
    side_b = parse_value(side_b)

    if side_a <= 0 or side_b <= 0:
        raise ValueError(
            "Side lengths must be positive."
        )

    return simplify(
        2 * side_a +
        2 * side_b
    )


def quadrilateral_perimeter(
    side_a,
    side_b,
    side_c,
    side_d
):
    """
    Calculate the perimeter of any quadrilateral.
    """

    sides = [
        parse_value(side_a),
        parse_value(side_b),
        parse_value(side_c),
        parse_value(side_d)
    ]

    if any(
        side <= 0
        for side in sides
    ):
        raise ValueError(
            "Side lengths must be positive."
        )

    return simplify(
        sum(sides)
    )


# ============================================================
# GEOMETRIC TRANSFORMATIONS
# ============================================================

def translate_point(
    x,
    y,
    delta_x,
    delta_y
):
    """
    Translate a point.

    Returns:
        (x + dx, y + dy)
    """

    x = parse_value(x)
    y = parse_value(y)
    delta_x = parse_value(delta_x)
    delta_y = parse_value(delta_y)

    return (
        simplify(
            x + delta_x
        ),
        simplify(
            y + delta_y
        )
    )


def reflect_x_axis(
    x,
    y
):
    """
    Reflect a point across the x-axis.
    """

    x = parse_value(x)
    y = parse_value(y)

    return (
        x,
        -y
    )


def reflect_y_axis(
    x,
    y
):
    """
    Reflect a point across the y-axis.
    """

    x = parse_value(x)
    y = parse_value(y)

    return (
        -x,
        y
    )


def reflect_origin(
    x,
    y
):
    """
    Reflect a point through the origin.
    """

    x = parse_value(x)
    y = parse_value(y)

    return (
        -x,
        -y
    )


def rotate_point_90(
    x,
    y
):
    """
    Rotate a point 90 degrees
    counterclockwise around the origin.
    """

    x = parse_value(x)
    y = parse_value(y)

    return (
        -y,
        x
    )


def rotate_point_180(
    x,
    y
):
    """
    Rotate a point 180 degrees
    around the origin.
    """

    x = parse_value(x)
    y = parse_value(y)

    return (
        -x,
        -y
    )


def rotate_point_270(
    x,
    y
):
    """
    Rotate a point 270 degrees
    counterclockwise around the origin.
    """

    x = parse_value(x)
    y = parse_value(y)

    return (
        y,
        -x
    )


def rotate_point(
    x,
    y,
    angle_degrees
):
    """
    Rotate a point counterclockwise around
    the origin by an arbitrary angle.

    Angle is given in degrees.
    """

    from sympy import cos, sin

    x = parse_value(x)
    y = parse_value(y)
    angle_degrees = parse_value(
        angle_degrees
    )

    angle_radians = (
        angle_degrees *
        pi / 180
    )

    new_x = simplify(
        x * cos(angle_radians) -
        y * sin(angle_radians)
    )

    new_y = simplify(
        x * sin(angle_radians) +
        y * cos(angle_radians)
    )

    return (
        new_x,
        new_y
    )


def dilate_point(
    x,
    y,
    scale_factor
):
    """
    Dilate a point from the origin.
    """

    x = parse_value(x)
    y = parse_value(y)
    scale_factor = parse_value(
        scale_factor
    )

    return (
        simplify(
            x * scale_factor
        ),
        simplify(
            y * scale_factor
        )
    )


def dilate_point_about_center(
    x,
    y,
    center_x,
    center_y,
    scale_factor
):
    """
    Dilate a point about an arbitrary center.
    """

    x = parse_value(x)
    y = parse_value(y)

    center_x = parse_value(
        center_x
    )

    center_y = parse_value(
        center_y
    )

    scale_factor = parse_value(
        scale_factor
    )

    new_x = simplify(
        center_x +
        scale_factor *
        (x - center_x)
    )

    new_y = simplify(
        center_y +
        scale_factor *
        (y - center_y)
    )

    return (
        new_x,
        new_y
    )


def translate_points(
    points,
    delta_x,
    delta_y
):
    """
    Translate a collection of points.
    """

    return [
        translate_point(
            x,
            y,
            delta_x,
            delta_y
        )
        for x, y in points
    ]


# ============================================================
# SIMILARITY AND SCALE
# ============================================================

def scale_factor(
    original_length,
    new_length
):
    """
    Calculate scale factor.

    Formula:
        k = new / original
    """

    original_length = parse_value(
        original_length
    )

    new_length = parse_value(
        new_length
    )

    if original_length == 0:
        raise ValueError(
            "Original length cannot be zero."
        )

    return simplify(
        new_length /
        original_length
    )


def similar_figure_length(
    original_length,
    scale_factor_value
):
    """
    Scale a length in a similar figure.
    """

    original_length = parse_value(
        original_length
    )

    scale_factor_value = parse_value(
        scale_factor_value
    )

    return simplify(
        original_length *
        scale_factor_value
    )


def similar_figure_area(
    original_area,
    scale_factor_value
):
    """
    Scale area using:

        A_new = A_original * k^2
    """

    original_area = parse_value(
        original_area
    )

    scale_factor_value = parse_value(
        scale_factor_value
    )

    return simplify(
        original_area *
        scale_factor_value**2
    )


def similar_figure_volume(
    original_volume,
    scale_factor_value
):
    """
    Scale volume using:

        V_new = V_original * k^3
    """

    original_volume = parse_value(
        original_volume
    )

    scale_factor_value = parse_value(
        scale_factor_value
    )

    return simplify(
        original_volume *
        scale_factor_value**3
    )


# ============================================================
# ADDITIONAL 3D GEOMETRY
# ============================================================

def triangular_prism_volume(
    triangle_base,
    triangle_height,
    prism_length
):
    """
    Calculate triangular prism volume.
    """

    triangle_base = parse_value(
        triangle_base
    )

    triangle_height = parse_value(
        triangle_height
    )

    prism_length = parse_value(
        prism_length
    )

    if (
        triangle_base <= 0 or
        triangle_height <= 0 or
        prism_length <= 0
    ):
        raise ValueError(
            "All dimensions must be positive."
        )

    base_area = (
        triangle_base *
        triangle_height / 2
    )

    return simplify(
        base_area *
        prism_length
    )


def triangular_prism_surface_area(
    side_a,
    side_b,
    side_c,
    triangle_base,
    triangle_height,
    prism_length
):
    """
    Calculate total surface area of
    a triangular prism.
    """

    side_a = parse_value(side_a)
    side_b = parse_value(side_b)
    side_c = parse_value(side_c)

    triangle_base = parse_value(
        triangle_base
    )

    triangle_height = parse_value(
        triangle_height
    )

    prism_length = parse_value(
        prism_length
    )

    if not triangle_is_valid(
        side_a,
        side_b,
        side_c
    ):
        raise ValueError(
            "The triangular base is invalid."
        )

    triangle_area_value = (
        triangle_base *
        triangle_height / 2
    )

    triangle_perimeter_value = (
        side_a +
        side_b +
        side_c
    )

    return simplify(
        2 * triangle_area_value +
        triangle_perimeter_value *
        prism_length
    )


def prism_surface_area(
    base_area,
    base_perimeter,
    height
):
    """
    Calculate total surface area
    of a right prism.

    Formula:
        SA = 2B + Ph
    """

    base_area = parse_value(base_area)

    base_perimeter = parse_value(
        base_perimeter
    )

    height = parse_value(height)

    if (
        base_area <= 0 or
        base_perimeter <= 0 or
        height <= 0
    ):
        raise ValueError(
            "All dimensions must be positive."
        )

    return simplify(
        2 * base_area +
        base_perimeter * height
    )


def pyramid_volume(
    base_area,
    height
):
    """
    Calculate general pyramid volume.

    Formula:
        V = Bh/3
    """

    base_area = parse_value(base_area)
    height = parse_value(height)

    if base_area <= 0 or height <= 0:
        raise ValueError(
            "Base area and height must be positive."
        )

    return simplify(
        base_area *
        height / 3
    )


def rectangular_pyramid_volume(
    length,
    width,
    height
):
    """
    Calculate rectangular pyramid volume.
    """

    length = parse_value(length)
    width = parse_value(width)
    height = parse_value(height)

    if (
        length <= 0 or
        width <= 0 or
        height <= 0
    ):
        raise ValueError(
            "All dimensions must be positive."
        )

    return simplify(
        length *
        width *
        height / 3
    )


def cone_slant_height(
    radius,
    height
):
    """
    Calculate cone slant height.

    Formula:
        l = sqrt(r^2 + h^2)
    """

    radius = parse_value(radius)
    height = parse_value(height)

    if radius <= 0 or height <= 0:
        raise ValueError(
            "Radius and height must be positive."
        )

    return simplify(
        sqrt(
            radius**2 +
            height**2
        )
    )


def cylinder_lateral_area(
    radius,
    height
):
    """
    Calculate lateral surface area
    of a cylinder.

    Formula:
        LA = 2*pi*r*h
    """

    radius = parse_value(radius)
    height = parse_value(height)

    if radius <= 0 or height <= 0:
        raise ValueError(
            "Radius and height must be positive."
        )

    return simplify(
        2 *
        pi *
        radius *
        height
    )


def cone_lateral_area(
    radius,
    height
):
    """
    Calculate lateral area of a cone.
    """

    radius = parse_value(radius)
    height = parse_value(height)

    slant_height = cone_slant_height(
        radius,
        height
    )

    return simplify(
        pi *
        radius *
        slant_height
    )


def hemisphere_curved_surface_area(
    radius
):
    """
    Calculate curved surface area
    of a hemisphere.

    Formula:
        SA = 2*pi*r^2
    """

    radius = parse_value(radius)

    if radius <= 0:
        raise ValueError(
            "Radius must be positive."
        )

    return simplify(
        2 *
        pi *
        radius**2
    )


def cone_frustum_volume(
    radius_1,
    radius_2,
    height
):
    """
    Calculate volume of a cone frustum.

    Formula:
        V = pi*h/3 *
            (R^2 + Rr + r^2)
    """

    radius_1 = parse_value(radius_1)
    radius_2 = parse_value(radius_2)
    height = parse_value(height)

    if (
        radius_1 <= 0 or
        radius_2 <= 0 or
        height <= 0
    ):
        raise ValueError(
            "Radii and height must be positive."
        )

    return simplify(
        pi *
        height / 3 *
        (
            radius_1**2 +
            radius_1 * radius_2 +
            radius_2**2
        )
    )


def cone_frustum_surface_area(
    radius_1,
    radius_2,
    height
):
    """
    Calculate total surface area
    of a cone frustum.
    """

    radius_1 = parse_value(radius_1)
    radius_2 = parse_value(radius_2)
    height = parse_value(height)

    if (
        radius_1 <= 0 or
        radius_2 <= 0 or
        height <= 0
    ):
        raise ValueError(
            "Radii and height must be positive."
        )

    slant_height = sqrt(
        height**2 +
        (
            radius_1 -
            radius_2
        )**2
    )

    return simplify(
        pi *
        (
            radius_1 +
            radius_2
        ) *
        slant_height
        +
        pi * radius_1**2
        +
        pi * radius_2**2
    )


def regular_tetrahedron_volume(
    side
):
    """
    Calculate volume of a regular tetrahedron.

    Formula:
        V = s^3 / (6*sqrt(2))
    """

    side = parse_value(side)

    if side <= 0:
        raise ValueError(
            "Side length must be positive."
        )

    return simplify(
        side**3 /
        (
            6 *
            sqrt(2)
        )
    )


def regular_tetrahedron_surface_area(
    side
):
    """
    Calculate surface area of a
    regular tetrahedron.

    Formula:
        SA = sqrt(3)*s^2
    """

    side = parse_value(side)

    if side <= 0:
        raise ValueError(
            "Side length must be positive."
        )

    return simplify(
        sqrt(3) *
        side**2
    )


# ============================================================
# GEOMETRY VALIDATION HELPERS
# ============================================================

def require_positive(
    value,
    name="Value"
):
    """
    Validate that a numeric geometric
    quantity is positive.
    """

    value = parse_value(value)

    if value <= 0:
        raise ValueError(
            f"{name} must be positive."
        )

    return value


def require_nonnegative(
    value,
    name="Value"
):
    """
    Validate that a numeric geometric
    quantity is nonnegative.
    """

    value = parse_value(value)

    if value < 0:
        raise ValueError(
            f"{name} cannot be negative."
        )

    return value


def require_polygon_sides(
    number_of_sides
):
    """
    Validate polygon side count.
    """

    number_of_sides = parse_value(
        number_of_sides
    )

    if number_of_sides.is_integer is not True:
        raise ValueError(
            "Number of sides must be an integer."
        )

    if number_of_sides < 3:
        raise ValueError(
            "A polygon must have at least 3 sides."
        )

    return number_of_sides


def require_triangle_angles(
    angle_1,
    angle_2,
    angle_3
):
    """
    Validate three interior triangle angles.
    """

    angle_1 = parse_value(angle_1)
    angle_2 = parse_value(angle_2)
    angle_3 = parse_value(angle_3)

    if not triangle_angle_sum_is_valid(
        angle_1,
        angle_2,
        angle_3
    ):
        raise ValueError(
            "The provided angles do not form a valid triangle."
        )

    return (
        angle_1,
        angle_2,
        angle_3
    )