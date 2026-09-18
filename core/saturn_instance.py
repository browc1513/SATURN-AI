from core.saturn_personality import SATURN


def get_saturn(config_path=None):
    """
    Return a S.A.T.U.R.N. instance.

    If no custom config path is supplied, allow SATURN to use
    its normal default configuration.
    """

    if config_path is None:
        return SATURN()

    return SATURN(
        config_path=config_path
    )
