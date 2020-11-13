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


def generate_competitor_preview(config):
    # Create a desired directory structure
    subprocess.check_output('git clone {} /tmp/competition'.format(config['competition']), shell=True)
    os.makedirs('/tmp/comeptition/controllers/participant_controller', exist_ok=True)
    subprocess.check_output('mv $(ls -A) /tmp/comeptition/controllers/participant_controller', shell=True)
    subprocess.check_output('mv $(ls -dA /tmp/comeptition/*) .', shell=True)

    subprocess.check_output('gh issue create --title "I found a bug" --body "Nothing works"', shell=True)
