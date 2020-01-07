import os
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_config(mode='dev'):
    config_path = os.path.join(
        BASE_DIR,
        '{}.yaml'.format(mode)
    )

    with open(config_path) as f:
        config = yaml.safe_load(f)
    return config
