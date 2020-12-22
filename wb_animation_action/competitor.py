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

import os
import shutil
import subprocess
from wb_animation_action.config import COMPETITION_TIMEOUT
from wb_animation_action.utils.webots import load_config, compile_controllers
from wb_animation_action.animation import generate_animation_for_world
from wb_animation_action.utils.git import push_directory_to_branch


def generate_competitor_preview(config):
    competition_url = config['competition']
    base = '/tmp/competition/'

    # Create a desired directory structure
    subprocess.check_output(f'git clone {competition_url} {base}', shell=True)
    os.makedirs(os.path.join(base, 'controllers/participant_controller'), exist_ok=True)
    shutil.copytree('.', os.path.join(base, 'controllers/participant_controller'))

    # Generate animation
    competition_config = load_config('webots.yaml')
    compile_controllers(base=base)
    generate_animation_for_world(os.path.join(base, competition_config['world']), COMPETITION_TIMEOUT)
    push_directory_to_branch('/tmp/animation', clean=True)
