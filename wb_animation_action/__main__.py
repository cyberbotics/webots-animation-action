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
    config = load_config()

    # Fire init-hook (usually dependencies)
    out = subprocess.check_output(config['init'], shell=True)
    print(out.decode('utf-8'))

    # Continue parsing
    if 'competition' in config:
        generate_competition(config['competition'])
    elif 'animation' in config:
        generate_animation(config['animation'])


if __name__ == "__main__":
    main()
