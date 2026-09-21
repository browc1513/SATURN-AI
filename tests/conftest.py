import pytest


SATURN_MODEL_ENVIRONMENT_VARIABLES = (
    "SATURN_LOCAL_MODEL_ENABLED",
    "SATURN_LOCAL_MODEL_NAME",
    "SATURN_LOCAL_MODEL_URL",
    "SATURN_LOCAL_MODEL_TIMEOUT",
    "SATURN_LOCAL_MODEL_SYSTEM_PROMPT",
)


@pytest.fixture(autouse=True)
def isolate_saturn_model_environment(
    monkeypatch,
):
    """
    Prevent per-machine model settings from changing test results.

    Individual tests can still enable environment overrides after
    this fixture clears the inherited host environment.
    """

    for variable in (
        SATURN_MODEL_ENVIRONMENT_VARIABLES
    ):
        monkeypatch.delenv(
            variable,
            raising=False,
        )
