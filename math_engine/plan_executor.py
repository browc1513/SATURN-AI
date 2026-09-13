"""
S.A.T.U.R.N. Plan Executor v1

Purpose
-------
Execute a structured problem plan one deterministic step at a time.

The executor:
    - resolves references such as "$radius"
    - calls the existing deterministic math executor
    - stores each step result for later steps
    - returns the completed plan and saved values
"""

from math_engine.executor import execute_math_operation
from math_engine.step_engine import generate_steps


def _resolve_reference(value, context):
    """
    Resolve a single "$name" reference from prior step results.
    """

    if (
        isinstance(value, str)
        and value.startswith("$")
    ):

        key = value[1:]

        if key not in context:
            raise KeyError(
                f"Unknown plan reference: {value}"
            )

        return context[key]

    return value


def _resolve_arguments(arguments, context):
    """
    Resolve all top-level plan references in an argument dictionary.
    """

    resolved = {}

    for name, value in arguments.items():

        resolved[name] = _resolve_reference(
            value,
            context,
        )

    return resolved


def execute_math_plan(plan):
    """
    Execute a plan created by problem_planner.plan_math_problem().
    """

    result = {
        "success": False,
        "goal": plan.get("goal"),
        "steps": [],
        "saved_results": {},
        "exact_result": None,
        "decimal_result": None,
        "error": None,
    }

    if not plan.get("success"):

        result["error"] = (
            plan.get("error")
            or "Cannot execute an unsuccessful plan."
        )

        return result

    context = {}

    for step in plan.get("steps", []):

        operation_name = step["operation"]

        try:
            arguments = _resolve_arguments(
                step.get(
                    "arguments",
                    {},
                ),
                context,
            )

        except KeyError as error:

            result["error"] = str(error)

            return result

        execution = execute_math_operation(
            operation_name,
            arguments,
        )

        if not execution.get("success"):

            result["error"] = (
                f"Step {step['step']} failed: "
                f"{execution.get('error')}"
            )

            return result

        exact_result = execution.get(
            "exact_result"
        )

        decimal_result = execution.get(
            "decimal_result"
        )

        step_result = generate_steps(
            operation_name=operation_name,
            arguments=arguments,
            exact_result=exact_result,
        )

        completed_step = {
            "step": step["step"],
            "source_text": step.get(
                "source_text"
            ),
            "operation": operation_name,
            "arguments": arguments,
            "save_as": step.get("save_as"),
            "exact_result": exact_result,
            "decimal_result": decimal_result,
            "steps": (
                step_result.get("steps", [])
                if step_result.get("success")
                else []
            ),
        }

        result["steps"].append(
            completed_step
        )

        save_as = step.get("save_as")

        if save_as:
            context[save_as] = exact_result

        result["exact_result"] = (
            exact_result
        )

        result["decimal_result"] = (
            decimal_result
        )

    result["saved_results"] = context
    result["success"] = True

    return result
