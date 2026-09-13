from math_engine.registry import math_registry


print("\n==============================")
print("S.A.T.U.R.N. Math Registry Test")
print("==============================")


print(
    "Total registered operations ->",
    len(math_registry.names())
)

print(
    "Arithmetic operations ->",
    len(
        math_registry.by_subsystem(
            "arithmetic"
        )
    )
)

print(
    "Algebra operations ->",
    len(
        math_registry.by_subsystem(
            "algebra"
        )
    )
)

print(
    "Solve equation exists ->",
    math_registry.exists(
        "solve_equation"
    )
)

print(
    "Factor expression exists ->",
    math_registry.exists(
        "factor_expression"
    )
)

print(
    "Search 'quadratic' ->",
    [
        operation["name"]
        for operation
        in math_registry.search(
            "quadratic"
        )
    ]
)

print(
    "Search 'domain' ->",
    [
        operation["name"]
        for operation
        in math_registry.search(
            "domain"
        )
    ]
)

print(
    "Arithmetic execution ->",
    math_registry.get(
        "add"
    )["function"](5, 7)
)

print(
    "Algebra execution ->",
    math_registry.get(
        "simplify_expression"
    )["function"](
        "(x**2 - 1)/(x - 1)"
    )
)


print(
    "Geometry operations ->",
    len(
        math_registry.by_subsystem(
            "geometry"
        )
    )
)

print(
    "Circle area exists ->",
    math_registry.exists(
        "circle_area"
    )
)

print(
    "Sphere volume exists ->",
    math_registry.exists(
        "sphere_volume"
    )
)

print(
    "Search 'circumradius' ->",
    [
        operation["name"]
        for operation
        in math_registry.search(
            "circumradius"
        )
    ]
)

print(
    "Geometry execution ->",
    math_registry.get(
        "rectangle_area"
    )["function"](5, 3)
)


print(
    "Trigonometry operations ->",
    len(
        math_registry.by_subsystem(
            "trigonometry"
        )
    )
)

print(
    "Trig expression utility exists ->",
    math_registry.exists(
        "trig_expression_value"
    )
)

print(
    "Trig rewrite utility exists ->",
    math_registry.exists(
        "rewrite_trig_as_sin_cos"
    )
)

print(
    "Search 'triangle' in Trigonometry ->",
    [
        operation["name"]
        for operation
        in math_registry.by_subsystem(
            "trigonometry"
        )
        if "triangle" in (
            operation["name"]
            + " "
            + operation["description"]
            + " "
            + " ".join(
                operation["keywords"]
            )
        ).lower()
    ]
)

print(
    "Trig execution ->",
    math_registry.get(
        "trig_expression_value"
    )["function"](
        "sin(pi/2)"
    )
)


print(
    "Calculus operations ->",
    len(
        math_registry.by_subsystem(
            "calculus"
        )
    )
)

print(
    "Derivative exists ->",
    math_registry.exists(
        "derivative"
    )
)

print(
    "Definite integral exists ->",
    math_registry.exists(
        "definite_integral"
    )
)

print(
    "Gradient vector exists ->",
    math_registry.exists(
        "gradient_vector"
    )
)

print(
    "Taylor series exists ->",
    math_registry.exists(
        "taylor_series"
    )
)

print(
    "Search 'derivative' in Calculus ->",
    [
        operation["name"]
        for operation
        in math_registry.by_subsystem(
            "calculus"
        )
        if "derivative" in (
            operation["name"]
            + " "
            + operation["description"]
            + " "
            + " ".join(
                operation["keywords"]
            )
        ).lower()
    ]
)

print(
    "Calculus execution ->",
    math_registry.get(
        "derivative"
    )["function"](
        "x**3",
        "x"
    )
)


print("\n==============================")
print("Registry Test Complete")
print("==============================")