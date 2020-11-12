#!/usr/bin/env python3
#
# Copyright 1996-2020 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
