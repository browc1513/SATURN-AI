from core.nova_personality import NOVA

# Optional: define a function to get a new N.O.V.A. instance with a custom config path
def get_nova(config_path=None):
    return NOVA(config_path=config_path)
