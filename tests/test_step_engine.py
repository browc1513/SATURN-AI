from sympy import pi

from math_engine.step_engine import generate_steps


print("\n==============================")
print("S.A.T.U.R.N. Step Engine Test")
print("==============================")


# ============================================================
# ADDITION
# ============================================================

result = generate_steps(
    operation_name="add",
    arguments={
        "a": 5,
        "b": 7
    },
    exact_result=12
)

print("\nAddition:")
print(result)


# ============================================================
# CIRCLE AREA
# ============================================================

result = generate_steps(
    operation_name="circle_area",
    arguments={
        "radius": 7
    },
    exact_result=49 * pi
)

print("\nCircle area:")
print(result)


# ============================================================
# SPHERE VOLUME
# ============================================================

result = generate_steps(
    operation_name="sphere_volume",
    arguments={
        "radius": 4
    },
    exact_result=256 * pi / 3
)

print("\nSphere volume:")
print(result)


# ============================================================
# DERIVATIVE
# ============================================================

result = generate_steps(
    operation_name="derivative",
    arguments={
        "expression": "x**3",
        "variable": "x"
    },
    exact_result="3*x**2"
)

print("\nDerivative:")
print(result)


# ============================================================
# SOLVE EQUATION
# ============================================================

result = generate_steps(
    operation_name="solve_equation",
    arguments={
        "equation": "x**2 - 4 = 0",
        "variable": "x"
    },
    exact_result=[-2, 2]
)

print("\nSolve equation:")
print(result)


# ============================================================
# UNSUPPORTED OPERATION
# ============================================================

result = generate_steps(
    operation_name="some_future_operation",
    arguments={
        "value": 10
    },
    exact_result=10
)

print("\nUnsupported operation:")
print(result)


# ============================================================
# MISSING INFORMATION
# ============================================================

result = generate_steps(
    operation_name="circle_area",
    arguments={},
    exact_result=None
)

print("\nMissing information:")
print(result)


print("\n==============================")
print("Step Engine Test Complete")
print("==============================")