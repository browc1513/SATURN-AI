from core.saturn_personality import SATURN


def get_saturn(
    config_path=None,
    start_alarm_monitor=True,
):
    """
    Return a S.A.T.U.R.N. instance.

    If no custom config path is supplied, allow SATURN to use
    its normal default configuration.

    Alarm monitoring is enabled by default so existing callers
    retain their current behavior. Interfaces that should not
    own alarm firing can disable it explicitly.
    """

    if config_path is None:
        return SATURN(
            start_alarm_monitor=start_alarm_monitor
        )

    return SATURN(
        config_path=config_path,
        start_alarm_monitor=start_alarm_monitor,
    )
