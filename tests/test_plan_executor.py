"""
S.A.T.U.R.N. Plan Executor v1 Test

Run:
    python -m tests.test_plan_executor
"""

from sympy import pi

from math_engine.plan_executor import (
    execute_math_plan,
)
from math_engine.problem_planner import (
    plan_math_problem,
)


def main():
    text = (
        "A circle has a circumference of 20*pi. "
        "Find its radius and then find its area."
    )

    print("=" * 72)
    print("S.A.T.U.R.N. Plan Executor v1 Test")
    print("=" * 72)
    print("Input:", text)

    plan = plan_math_problem(
        text
    )

    assert plan["success"], plan["error"]

    result = execute_math_plan(
        plan
    )

    print("\nSuccess:", result.get("success"))
    print("Error  :", result.get("error"))

    for step in result.get("steps", []):
        print(
            f"\nStep {step['step']}: "
            f"{step['operation']}"
        )
        print(
            "  arguments =",
            step["arguments"],
        )
        print(
            "  result    =",
            step["exact_result"],
        )
        print(
            "  save_as   =",
            step["save_as"],
        )

    print(
        "\nSaved results:",
        result.get("saved_results"),
    )

    assert result["success"], result["error"]

    assert (
        result["saved_results"]["radius"]
        == 10
    )

    assert (
        result["saved_results"]["area"]
        == 100 * pi
    )

    print("\nRESULT: PLAN EXECUTOR PASSED")


if __name__ == "__main__":
    main()
