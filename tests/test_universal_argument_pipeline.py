from math_engine.interpreter import interpret_math_request
from math_engine.router import select_math_operation
from math_engine.argument_extractor import (
    extract_arguments_for_operation,
)
from math_engine.executor import execute_math_operation


TESTS = [
    "Find the derivative of x**3 with respect to x.",
    "What is the area of a rectangle with width 7 and length 5?",
    "Find the volume of a cylinder with radius 4 and height 10.",
    "What is the area of a circle with radius 7?",
]


print("=" * 60)
print("S.A.T.U.R.N. Universal Argument Pipeline Test")
print("=" * 60)


for text in TESTS:

    print()
    print("-" * 60)
    print("INPUT:")
    print(text)

    interpretation = interpret_math_request(
        text
    )

    print()
    print("INTERPRETATION:")
    print(interpretation)

    routing = select_math_operation(
        query=interpretation["query"],
        subsystem=interpretation["subsystem"],
    )

    print()
    print("ROUTING:")
    print(routing)

    if not routing["success"]:
        print()
        print("FAILED AT ROUTING")
        continue

    operation_name = routing[
        "operation"
    ]

    extraction = extract_arguments_for_operation(
        text,
        operation_name,
    )

    print()
    print("UNIVERSAL EXTRACTION:")
    print(extraction)

    if not extraction["success"]:
        print()
        print("FAILED AT ARGUMENT EXTRACTION")
        continue

    execution = execute_math_operation(
        operation_name,
        extraction["arguments"],
    )

    print()
    print("EXECUTION:")
    print(execution)


print()
print("=" * 60)
print("Universal Argument Pipeline Test Complete")
print("=" * 60)