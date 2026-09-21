import os

import pytest


SATURN_MODEL_ENVIRONMENT_VARIABLES = (
    "SATURN_LOCAL_MODEL_ENABLED",
    "SATURN_LOCAL_MODEL_NAME",
    "SATURN_LOCAL_MODEL_URL",
    "SATURN_LOCAL_MODEL_TIMEOUT",
    "SATURN_LOCAL_MODEL_SYSTEM_PROMPT",
)


@pytest.fixture(
    scope="session",
    autouse=True,
)
def isolate_saturn_model_environment():
    """
    Keep machine-specific model settings out of the complete test run.

    Session scope ensures environment isolation occurs before any
    module-scoped SATURN fixtures are created.
    """

    original_values = {
        variable: os.environ.get(variable)
        for variable in SATURN_MODEL_ENVIRONMENT_VARIABLES
    }

    for variable in (
        SATURN_MODEL_ENVIRONMENT_VARIABLES
    ):
        os.environ.pop(
            variable,
            None,
        )

    yield

    for variable, value in original_values.items():
        if value is None:
            os.environ.pop(
                variable,
                None,
            )
        else:
            os.environ[variable] = value
