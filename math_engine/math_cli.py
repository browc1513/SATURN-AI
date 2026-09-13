from math_engine.math_pipeline import interpret_and_execute_math


def print_header():
    print()
    print("=" * 44)
    print("              S.A.T.U.R.N. MATH")
    print("=" * 44)
    print("Type a math question.")
    print("Type 'exit' or 'quit' to close SATURN.")
    print()


def print_result(result):
    """
    Print a clean user-facing response from the
    natural-language math pipeline.
    """

    if not result["success"]:

        print("\nSATURN:")

        if result["error"]:
            print(f"Error: {result['error']}")

        if result["warnings"]:
            for warning in result["warnings"]:
                print(f"Warning: {warning}")

        print()

        return

    print("\nSATURN:\n")

    steps = result.get(
        "steps",
        []
    )

    if steps:

        for step_number, step in enumerate(
            steps,
            start=1
        ):
            print(
                f"{step_number}. {step}"
            )

        print()

    exact_result = result.get(
        "exact_result"
    )

    decimal_result = result.get(
        "decimal_result"
    )

    if exact_result is not None:
        print(
            f"Exact Answer: {exact_result}"
        )

    if (
        decimal_result is not None
        and decimal_result != exact_result
    ):
        print(
            f"Decimal Answer: {decimal_result}"
        )

    warnings = result.get(
        "warnings",
        []
    )

    if warnings:
        print()

        for warning in warnings:
            print(
                f"Warning: {warning}"
            )

    print()


def run_math_cli():
    """
    Start SATURN's interactive terminal math interface.
    """

    print_header()

    while True:

        try:

            user_input = input(
                "You: "
            ).strip()

        except (
            KeyboardInterrupt,
            EOFError
        ):

            print(
                "\n\nSATURN: Goodbye."
            )

            break

        if user_input.lower() in (
            "exit",
            "quit"
        ):

            print(
                "\nSATURN: Goodbye."
            )

            break

        if not user_input:

            print(
                "\nSATURN: Please enter a math question.\n"
            )

            continue

        result = interpret_and_execute_math(
            user_input
        )

        print_result(
            result
        )


if __name__ == "__main__":
    run_math_cli()