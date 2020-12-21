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
import subprocess
from wb_animation_action.config import COMPETITION_TIMEOUT
from wb_animation_action.utils.webots import load_config
from wb_animation_action.animation import generate_animation_for_world
from wb_animation_action.utils.git import push_directory_to_branch


def generate_competitor_preview(config):
    competition_url = config['competition']

    # Create a desired directory structure
    subprocess.check_output(f'git clone {competition_url} /tmp/competition', shell=True)
    os.makedirs('/tmp/competition/controllers/participant_controller', exist_ok=True)
    subprocess.check_output('mv $(ls -A) /tmp/competition/controllers/participant_controller', shell=True)
    subprocess.check_output('mv $(ls -dA /tmp/competition/*) .', shell=True)

    # Generate animation
    competition_config = load_config('controllers/participant_controller/webots.yaml')
    generate_animation_for_world(competition_config['world'], COMPETITION_TIMEOUT)
    push_directory_to_branch('/tmp/competition', clean=True)
