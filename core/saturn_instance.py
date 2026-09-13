from core.saturn_personality import SATURN

# Optional: define a function to get a new S.A.T.U.R.N. instance with a custom config path
def get_saturn(config_path=None):
    return SATURN(config_path=config_path)
