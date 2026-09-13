"""
S.A.T.U.R.N. Problem Planner v1 Test

Run:
    python -m tests.test_problem_planner
"""

from math_engine.problem_planner import (
    plan_math_problem,
)


def main():
    text = (
        "A circle has a circumference of 20*pi. "
        "Find its radius and then find its area."
    )

    print("=" * 72)
    print("S.A.T.U.R.N. Problem Planner v1 Test")
    print("=" * 72)
    print("Input:", text)

    plan = plan_math_problem(
        text
    )

    print("\nSuccess:", plan.get("success"))
    print("Error  :", plan.get("error"))
    print("Goal   :", plan.get("goal"))

    print("\nPlanned steps:")

    for step in plan.get("steps", []):
        print(
            f"  Step {step['step']}: "
            f"{step['operation']}"
        )
        print(
            f"    arguments = "
            f"{step['arguments']}"
        )
        print(
            f"    save_as   = "
            f"{step['save_as']}"
        )

    assert plan["success"], plan["error"]
    assert len(plan["steps"]) == 2

    assert (
        plan["steps"][0]["operation"]
        == "circle_radius_from_circumference"
    )

    assert (
        plan["steps"][0]["arguments"][
            "circumference"
        ]
        == "20*pi"
    )

    assert (
        plan["steps"][0]["save_as"]
        == "radius"
    )

    assert (
        plan["steps"][1]["operation"]
        == "circle_area"
    )

    assert (
        plan["steps"][1]["arguments"][
            "radius"
        ]
        == "$radius"
    )

    print("\nRESULT: PROBLEM PLANNER PASSED")


if __name__ == "__main__":
    main()
