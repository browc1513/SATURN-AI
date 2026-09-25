import os

import pytest


SATURN_TEST_ALARM_MONITOR_VARIABLE = (
    "SATURN_DISABLE_ALARM_MONITOR"
)


def pytest_configure(config):
    """
    Disable real background alarm monitoring before pytest imports
    test modules. This prevents collection-time imports from starting
    threads that can mutate isolated alarm files during other tests.
    """

    original_value = os.environ.get(
        SATURN_TEST_ALARM_MONITOR_VARIABLE
    )

    setattr(
        config,
        "_saturn_original_alarm_monitor_setting",
        original_value,
    )

    os.environ[
        SATURN_TEST_ALARM_MONITOR_VARIABLE
    ] = "true"


def pytest_unconfigure(config):
    original_value = getattr(
        config,
        "_saturn_original_alarm_monitor_setting",
        None,
    )

    if original_value is None:
        os.environ.pop(
            SATURN_TEST_ALARM_MONITOR_VARIABLE,
            None,
        )
    else:
        os.environ[
            SATURN_TEST_ALARM_MONITOR_VARIABLE
        ] = original_value


SATURN_MODEL_ENVIRONMENT_VARIABLES = (
    "SATURN_LOCAL_MODEL_ENABLED",
    "SATURN_LOCAL_MODEL_NAME",
    "SATURN_LOCAL_MODEL_URL",
    "SATURN_LOCAL_MODEL_TIMEOUT",
    "SATURN_LOCAL_MODEL_SYSTEM_PROMPT",
    "SATURN_MEMORY_DATABASE",
    "SATURN_MEMORY_ENABLED",
    "SATURN_REBOOT_ENABLED",
    "SATURN_VOICE_COMMAND_TIMEOUT",
    "SATURN_VOICE_COMMAND_PHRASE_LIMIT",
    "SATURN_VOICE_FOLLOW_UP_TIMEOUT",
    "SATURN_VOICE_FOLLOW_UP_PHRASE_LIMIT",
    "SATURN_VOICE_PAUSE_THRESHOLD",
    "SATURN_VOICE_PHRASE_THRESHOLD",
    "SATURN_VOICE_NON_SPEAKING_DURATION",
    "SATURN_VOICE_AMBIENT_DURATION",
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
