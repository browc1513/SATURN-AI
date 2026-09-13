from math_engine.interpreter import interpret_math_request
from math_engine.router import select_math_operation


print()
print("=" * 52)
print("S.A.T.U.R.N. Route-First Test")
print("=" * 52)


tests = [
    (
        "What is the area of a rectangle "
        "with a width of 7 and a length of 5?"
    ),
    (
        "Find the volume of a cylinder "
        "with radius 4 and height 10."
    ),
    (
        "Find the volume of a sphere "
        "with radius 4."
    ),
    (
        "What is the area of a circle "
        "with radius 7?"
    ),
]


for text in tests:

    print()
    print("-" * 52)
    print("INPUT:")
    print(text)

    interpretation = interpret_math_request(
        text
    )

    print("\nINTERPRETATION:")
    print(interpretation)

    routing = select_math_operation(
        query=interpretation["query"],
        subsystem=interpretation["subsystem"],
    )

    print("\nROUTING:")
    print(routing)


print()
print("=" * 52)
print("Route-First Test Complete")
print("=" * 52)
print()