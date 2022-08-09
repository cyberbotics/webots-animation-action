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
from wb_animation_action.utils.webots import load_config
from wb_animation_action.animation import generate_animation
from wb_animation_action.competition import generate_competition
from wb_animation_action.competitor import generate_competitor_preview


def main():
    # Load config
    config = load_config()

    # Fire init-hook (usually dependencies)
    if 'init' in config:
        out = subprocess.check_output(config['init'], shell=True)
        print(out.decode('utf-8'))

    # Continue parsing
    if 'type' not in config or config['type'] != 'benchmark':
        print('You have to specify `type` parameter in `webots.yaml` and set it to `benchmark`')

    # generate animation from benchmark
    generate_animation(config['animation'])


if __name__ == "__main__":
    main()
