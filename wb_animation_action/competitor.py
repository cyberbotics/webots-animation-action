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
    competition_url = config['competition']
    username = os.environ['GITHUB_ACTOR']
    competitor_url = os.environ['GITHUB_REPOSITORY']
    
    # Create a desired directory structure
    subprocess.check_output(f'git clone {competition_url} /tmp/competition', shell=True)
    os.makedirs('/tmp/competition/controllers/participant_controller', exist_ok=True)
    subprocess.check_output('mv $(ls -A) /tmp/competition/controllers/participant_controller', shell=True)
    subprocess.check_output('mv $(ls -dA /tmp/competition/*) .', shell=True)

    subprocess.check_output(f'gh issue --repo {competition_url} create --label registration,{username} --title "User {username} wants to compete" --body "CompetitionUrl: {competitor_url}"', shell=True)
