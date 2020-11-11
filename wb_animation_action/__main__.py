import sys
import os
import subprocess
import yaml
from .animation import generate_animation
from .competition import generate_competition


def load_config():
    """Load config from webots.yaml located in the repository root."""

    config = None
    if os.path.isfile('webots.yaml'):
        with open('webots.yaml', 'r') as f:
            config = yaml.load(f.read(), Loader=yaml.FullLoader) or {}
    if config is None:
        print('Cannot load `webots.yaml`')
        sys.exit(1)
    return config


def main():
    # Load config
    config = load_config()

    # Fire init-hook (usually dependencies)
    if 'init' in config:
        out = subprocess.check_output(config['init'], shell=True)
        print(out.decode('utf-8'))

    # Continue parsing
    if 'type' not in config:
        print('You have to specify `type` parameter (`demo`, `competition` or `competitor`) in `webots.yaml`')

    if config['type'] == 'competition':
        generate_competition(config)
    elif config['type'] == 'demo':
        generate_animation(config['animation'])


if __name__ == "__main__":
    main()
