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
    regular_tetrahedron_surface_area,

    require_positive,
    require_nonnegative,
    require_polygon_sides,
    require_triangle_angles
)


print("\n==============================")
print("N.O.V.A. Geometry Test")
print("==============================")


# Rectangle
print("\nRectangle:")
print("Area of 5 x 3 ->", rectangle_area(5, 3))
print("Perimeter of 5 x 3 ->", rectangle_perimeter(5, 3))


# Square
print("\nSquare:")
print("Area with side 4 ->", square_area(4))
print("Perimeter with side 4 ->", square_perimeter(4))


# Triangle
print("\nTriangle:")
print("Area with base 10 and height 6 ->", triangle_area(10, 6))
print("Perimeter of 3, 4, 5 ->", triangle_perimeter(3, 4, 5))


# Circle
print("\nCircle:")
print("Area with radius 3 ->", circle_area(3))
print("Circumference with radius 3 ->", circle_circumference(3))


# Parallelogram
print("\nParallelogram:")
print(
    "Area with base 8 and height 5 ->",
    parallelogram_area(8, 5)
)


# Trapezoid
print("\nTrapezoid:")
print(
    "Area with bases 6 and 10, height 4 ->",
    trapezoid_area(6, 10, 4)
)


# Rhombus
print("\nRhombus:")
print(
    "Area with diagonals 8 and 6 ->",
    rhombus_area(8, 6)
)


# ============================================================
# COORDINATE GEOMETRY
# ============================================================

print("\nCoordinate Geometry:")

print(
    "Distance between (0, 0) and (3, 4) ->",
    distance_between_points(
        0, 0,
        3, 4
    )
)

print(
    "Midpoint of (2, 4) and (6, 8) ->",
    midpoint(
        2, 4,
        6, 8
    )
)

print(
    "Slope between (1, 2) and (3, 6) ->",
    slope(
        1, 2,
        3, 6
    )
)

print(
    "Line through (2, 5) with slope 3 ->",
    line_from_point_slope(
        2, 5,
        3
    )
)

print(
    "Line through (1, 3) and (3, 7) ->",
    line_from_two_points(
        1, 3,
        3, 7
    )
)

print(
    "Are slopes 2 and 2 parallel? ->",
    are_parallel(
        2,
        2
    )
)

print(
    "Are slopes 2 and -1/2 perpendicular? ->",
    are_perpendicular(
        2,
        "-1/2"
    )
)


# Undefined slope test
print("\nVertical Line Test:")

try:
    print(
        slope(
            2, 1,
            2, 5
        )
    )

except ValueError as error:
    print(
        "Correctly caught error:",
        error
    )


# ============================================================
# TRIANGLE GEOMETRY
# ============================================================

print("\nTriangle Geometry:")

print(
    "Hypotenuse with legs 3 and 4 ->",
    pythagorean_hypotenuse(
        3,
        4
    )
)

print(
    "Missing leg with hypotenuse 5 and leg 3 ->",
    pythagorean_leg(
        5,
        3
    )
)

print(
    "Are sides 3, 4, 5 valid? ->",
    triangle_is_valid(
        3,
        4,
        5
    )
)

print(
    "Are sides 1, 2, 10 valid? ->",
    triangle_is_valid(
        1,
        2,
        10
    )
)

print(
    "Area of 3-4-5 triangle using Heron's formula ->",
    heron_triangle_area(
        3,
        4,
        5
    )
)

print(
    "Third angle when two angles are 60 and 40 ->",
    missing_triangle_angle(
        60,
        40
    )
)

print(
    "Triangle 5, 5, 8 by sides ->",
    classify_triangle_by_sides(
        5,
        5,
        8
    )
)

print(
    "Triangle 5, 5, 5 by sides ->",
    classify_triangle_by_sides(
        5,
        5,
        5
    )
)

print(
    "Angles 30, 60, 90 ->",
    classify_triangle_by_angles(
        30,
        60,
        90
    )
)

print(
    "Angles 60, 60, 60 ->",
    classify_triangle_by_angles(
        60,
        60,
        60
    )
)

print(
    "Angles 30, 40, 110 ->",
    classify_triangle_by_angles(
        30,
        40,
        110
    )
)


# Invalid triangle test
print("\nInvalid Triangle Test:")

try:
    print(
        heron_triangle_area(
            1,
            2,
            10
        )
    )

except ValueError as error:
    print(
        "Correctly caught error:",
        error
    )


# ============================================================
# CIRCLES AND REGULAR POLYGONS
# ============================================================

print("\nCircles and Regular Polygons:")

print(
    "Diameter with radius 5 ->",
    circle_diameter(5)
)

print(
    "Arc length: radius 6, angle 90° ->",
    arc_length(
        6,
        90
    )
)

print(
    "Sector area: radius 6, angle 90° ->",
    sector_area(
        6,
        90
    )
)

print(
    "Semicircle area with radius 4 ->",
    semicircle_area(4)
)

print(
    "Annulus area with radii 5 and 3 ->",
    annulus_area(
        5,
        3
    )
)

print(
    "Regular hexagon perimeter with side 4 ->",
    regular_polygon_perimeter(
        6,
        4
    )
)

print(
    "Regular hexagon interior angle ->",
    regular_polygon_interior_angle(
        6
    )
)

print(
    "Pentagon interior angle sum ->",
    polygon_interior_angle_sum(
        5
    )
)

print(
    "Regular polygon area: n=6, side=4, apothem=2*sqrt(3) ->",
    regular_polygon_area_from_apothem(
        6,
        4,
        "2*sqrt(3)"
    )
)


# ============================================================
# 3D GEOMETRY / SOLID GEOMETRY
# ============================================================

print("\n3D Geometry:")

print(
    "Cube volume, side 3 ->",
    cube_volume(3)
)

print(
    "Cube surface area, side 3 ->",
    cube_surface_area(3)
)

print(
    "Rectangular prism volume 2 x 3 x 4 ->",
    rectangular_prism_volume(2, 3, 4)
)

print(
    "Rectangular prism surface area 2 x 3 x 4 ->",
    rectangular_prism_surface_area(2, 3, 4)
)

print(
    "Cylinder volume, r=3, h=5 ->",
    cylinder_volume(3, 5)
)

print(
    "Cylinder surface area, r=3, h=5 ->",
    cylinder_surface_area(3, 5)
)

print(
    "Cone volume, r=3, h=4 ->",
    cone_volume(3, 4)
)

print(
    "Cone surface area, r=3, h=4 ->",
    cone_surface_area(3, 4)
)

print(
    "Sphere volume, r=3 ->",
    sphere_volume(3)
)

print(
    "Sphere surface area, r=3 ->",
    sphere_surface_area(3)
)

print(
    "Hemisphere volume, r=3 ->",
    hemisphere_volume(3)
)

print(
    "Hemisphere total surface area, r=3 ->",
    hemisphere_surface_area(3)
)

print(
    "Square pyramid volume, side=6, height=4 ->",
    square_pyramid_volume(6, 4)
)

print(
    "Square pyramid surface area, side=6, slant height=5 ->",
    square_pyramid_surface_area(6, 5)
)

print(
    "General prism volume, base area=12, height=5 ->",
    prism_volume(12, 5)
)


# ============================================================
# LINE GEOMETRY
# ============================================================

print("\nLine Geometry:")

print(
    "Slope-intercept equation m=2, b=3 ->",
    line_equation_slope_intercept(2, 3)
)

print(
    "Point-slope equation through (1, 3), m=2 ->",
    line_equation_point_slope(1, 3, 2)
)

print(
    "Standard form through (1, 2) and (3, 6) ->",
    line_standard_form_from_points(1, 2, 3, 6)
)

print(
    "x-intercept of y=2x+4 ->",
    line_x_intercept(2, 4)
)

print(
    "y-intercept of y=2x+4 ->",
    line_y_intercept(2, 4)
)

print(
    "Intersection of y=2x+1 and y=-x+4 ->",
    line_intersection(2, 1, -1, 4)
)

print(
    "Distance from (0, 0) to 3x+4y-20=0 ->",
    point_to_line_distance(0, 0, 3, 4, -20)
)

print(
    "Perpendicular slope to 2 ->",
    perpendicular_slope(2)
)

print(
    "Perpendicular bisector of (0,0) and (4,4) ->",
    perpendicular_bisector(0, 0, 4, 4)
)


# ============================================================
# ADVANCED TRIANGLE GEOMETRY
# ============================================================

print("\nAdvanced Triangle Geometry:")

print(
    "Angles 60, 60, 60 valid? ->",
    triangle_angle_sum_is_valid(60, 60, 60)
)

print(
    "Angles 90, 60, 40 valid? ->",
    triangle_angle_sum_is_valid(90, 60, 40)
)

print(
    "Exterior angle from remote angles 50 and 60 ->",
    triangle_exterior_angle(50, 60)
)

print(
    "Triangle sides 3, 4, 5 by angles ->",
    classify_triangle_by_side_lengths(3, 4, 5)
)

print(
    "Triangle sides 5, 5, 6 by angles ->",
    classify_triangle_by_side_lengths(5, 5, 6)
)

print(
    "Equilateral triangle height, side 4 ->",
    equilateral_triangle_height(4)
)

print(
    "Equilateral triangle area, side 4 ->",
    equilateral_triangle_area(4)
)

print(
    "Isosceles triangle height, equal side 5, base 6 ->",
    isosceles_triangle_height(5, 6)
)

print(
    "Isosceles triangle area, equal side 5, base 6 ->",
    isosceles_triangle_area(5, 6)
)

print(
    "Centroid of (0,0), (6,0), (0,6) ->",
    triangle_centroid(0, 0, 6, 0, 0, 6)
)

print(
    "Inradius of 3-4-5 triangle ->",
    triangle_inradius_from_area(6, 3, 4, 5)
)

print(
    "Circumradius of 3-4-5 triangle ->",
    triangle_circumradius(3, 4, 5)
)


# ============================================================
# ADVANCED CIRCLE GEOMETRY
# ============================================================

print("\nAdvanced Circle Geometry:")

print(
    "Radius from diameter 10 ->",
    circle_radius_from_diameter(10)
)

print(
    "Radius from circumference 10*pi ->",
    circle_radius_from_circumference("10*pi")
)

print(
    "Radius from area 25*pi ->",
    circle_radius_from_area("25*pi")
)

print(
    "Circumference from diameter 8 ->",
    circle_circumference_from_diameter(8)
)

print(
    "Chord length, radius 5, center distance 3 ->",
    chord_length(5, 3)
)

print(
    "Center-to-chord distance, radius 5, chord 8 ->",
    center_to_chord_distance(5, 8)
)

print(
    "Circle equation center (2,-3), radius 5 ->",
    circle_equation(2, -3, 5)
)

print(
    "Circle center/radius from h=2, k=-3, r^2=25 ->",
    circle_center_radius_from_standard(2, -3, 25)
)


# ============================================================
# POLYGON GEOMETRY
# ============================================================

print("\nPolygon Geometry:")

print(
    "Exterior angle of regular hexagon ->",
    regular_polygon_exterior_angle(6)
)

print(
    "Exterior angle sum of any polygon ->",
    polygon_exterior_angle_sum()
)

print(
    "Number of diagonals in hexagon ->",
    polygon_diagonals(6)
)

print(
    "Apothem of square with side 4 ->",
    regular_polygon_apothem(4, 4)
)

print(
    "Area of square using regular polygon formula, side 4 ->",
    regular_polygon_area(4, 4)
)

print(
    "Side length of square with apothem 2 ->",
    regular_polygon_side_from_apothem(4, 2)
)

print(
    "Polygon with 8 sides ->",
    classify_polygon(8)
)

print(
    "Polygon with 15 sides ->",
    classify_polygon(15)
)

print(
    "Perimeter of sides [3, 4, 5] ->",
    polygon_perimeter([3, 4, 5])
)

print(
    "Shoelace area of rectangle ->",
    shoelace_area(
        [
            (0, 0),
            (4, 0),
            (4, 3),
            (0, 3)
        ]
    )
)


# ============================================================
# QUADRILATERAL GEOMETRY
# ============================================================

print("\nQuadrilateral Geometry:")

print(
    "Rectangle diagonal 3 x 4 ->",
    rectangle_diagonal(3, 4)
)

print(
    "Square diagonal, side 5 ->",
    square_diagonal(5)
)

print(
    "Rhombus perimeter, side 6 ->",
    rhombus_perimeter(6)
)

print(
    "Parallelogram perimeter, sides 5 and 8 ->",
    parallelogram_perimeter(5, 8)
)

print(
    "Trapezoid perimeter 3, 4, 5, 6 ->",
    trapezoid_perimeter(3, 4, 5, 6)
)

print(
    "Kite area, diagonals 8 and 6 ->",
    kite_area(8, 6)
)

print(
    "Kite perimeter, sides 5 and 7 ->",
    kite_perimeter(5, 7)
)

print(
    "Quadrilateral perimeter 2, 3, 4, 5 ->",
    quadrilateral_perimeter(2, 3, 4, 5)
)


# ============================================================
# GEOMETRIC TRANSFORMATIONS
# ============================================================

print("\nGeometric Transformations:")

print(
    "Translate (2,3) by (4,-1) ->",
    translate_point(2, 3, 4, -1)
)

print(
    "Reflect (2,3) across x-axis ->",
    reflect_x_axis(2, 3)
)

print(
    "Reflect (2,3) across y-axis ->",
    reflect_y_axis(2, 3)
)

print(
    "Reflect (2,3) across origin ->",
    reflect_origin(2, 3)
)

print(
    "Rotate (2,3) 90 degrees ->",
    rotate_point_90(2, 3)
)

print(
    "Rotate (2,3) 180 degrees ->",
    rotate_point_180(2, 3)
)

print(
    "Rotate (2,3) 270 degrees ->",
    rotate_point_270(2, 3)
)

print(
    "Rotate (1,0) 45 degrees ->",
    rotate_point(1, 0, 45)
)

print(
    "Dilate (2,3) by factor 2 ->",
    dilate_point(2, 3, 2)
)

print(
    "Dilate (3,3) about (1,1) by factor 2 ->",
    dilate_point_about_center(3, 3, 1, 1, 2)
)

print(
    "Translate multiple points ->",
    translate_points(
        [(0, 0), (1, 2), (3, 4)],
        2,
        -1
    )
)


# ============================================================
# SIMILARITY AND SCALE
# ============================================================

print("\nSimilarity and Scale:")

print(
    "Scale factor from 4 to 10 ->",
    scale_factor(4, 10)
)

print(
    "Length 6 scaled by factor 3 ->",
    similar_figure_length(6, 3)
)

print(
    "Area 10 scaled by factor 3 ->",
    similar_figure_area(10, 3)
)

print(
    "Volume 10 scaled by factor 3 ->",
    similar_figure_volume(10, 3)
)


# ============================================================
# ADDITIONAL 3D GEOMETRY
# ============================================================

print("\nAdditional 3D Geometry:")

print(
    "Triangular prism volume, triangle 6x4, length 10 ->",
    triangular_prism_volume(6, 4, 10)
)

print(
    "Triangular prism surface area, 3-4-5 base, height 3, length 10 ->",
    triangular_prism_surface_area(
        3,
        4,
        5,
        4,
        3,
        10
    )
)

print(
    "General prism surface area, B=12, P=14, h=5 ->",
    prism_surface_area(12, 14, 5)
)

print(
    "General pyramid volume, B=30, h=6 ->",
    pyramid_volume(30, 6)
)

print(
    "Rectangular pyramid volume 4x6x9 ->",
    rectangular_pyramid_volume(4, 6, 9)
)

print(
    "Cone slant height, r=3, h=4 ->",
    cone_slant_height(3, 4)
)

print(
    "Cylinder lateral area, r=3, h=5 ->",
    cylinder_lateral_area(3, 5)
)

print(
    "Cone lateral area, r=3, h=4 ->",
    cone_lateral_area(3, 4)
)

print(
    "Hemisphere curved surface area, r=3 ->",
    hemisphere_curved_surface_area(3)
)

print(
    "Cone frustum volume, R=5, r=3, h=4 ->",
    cone_frustum_volume(5, 3, 4)
)

print(
    "Cone frustum total surface area, R=5, r=3, h=4 ->",
    cone_frustum_surface_area(5, 3, 4)
)

print(
    "Regular tetrahedron volume, side 6 ->",
    regular_tetrahedron_volume(6)
)

print(
    "Regular tetrahedron surface area, side 6 ->",
    regular_tetrahedron_surface_area(6)
)


# ============================================================
# VALIDATION HELPERS
# ============================================================

print("\nGeometry Validation:")

print(
    "Positive value 5 ->",
    require_positive(5, "Length")
)

print(
    "Nonnegative value 0 ->",
    require_nonnegative(0, "Radius")
)

print(
    "Valid polygon side count 6 ->",
    require_polygon_sides(6)
)

print(
    "Valid triangle angles 30, 60, 90 ->",
    require_triangle_angles(30, 60, 90)
)


print("\nValidation Error Tests:")

try:
    require_positive(-5, "Length")
except ValueError as error:
    print(
        "Correctly caught negative length:",
        error
    )

try:
    require_polygon_sides(2)
except ValueError as error:
    print(
        "Correctly caught invalid polygon:",
        error
    )

try:
    require_triangle_angles(90, 90, 90)
except ValueError as error:
    print(
        "Correctly caught invalid triangle angles:",
        error
    )


print("\n==============================")
print("Geometry Test Complete")
print("==============================")