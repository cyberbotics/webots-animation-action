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

import subprocess
import os
from glob import glob
import requests
from wb_animation_action.utils.utils import is_debug, remove_anything


def _init():
    username = os.environ['GITHUB_ACTOR']
    user_info = requests.get(f'https://api.github.com/users/{username}').json()

    result = subprocess.run('git config --list | grep user.name', shell=True, check=False)
    if result.returncode != 0:
        email = '{}+{}@users.noreply.github.com'.format(user_info['id'], username)
        subprocess.check_output(['git', 'config', '--global', 'user.name', user_info['name'] or username])
        subprocess.check_output(['git', 'config', '--global', 'user.email', email])


def push(message='Updated animation', force=True):
    _init()

    github_repository = 'https://{}:{}@github.com/{}'.format(
        os.environ['GITHUB_ACTOR'],
        os.environ['GITHUB_TOKEN'],
        os.environ['GITHUB_REPOSITORY']
    )

    subprocess.check_output(['git', 'add', '-A'])
    subprocess.check_output(['git', 'commit', '-m', message])
    if not is_debug():
        params = ['git', 'push']
        if force:
            params += ['-f']
        params += [github_repository]
        subprocess.check_output(params)
    else:
        print(f'@ git push {github_repository}')


def push_directory_to_branch(source_directory, destination_directory='.', destination_branch='gh-pages', clean=False):
    """Publishes an arbitrary dictionary to a new branch (usually `gh-pages`)."""

    _init()

    subprocess.check_output(['git', 'reset', '--hard'])
    subprocess.check_output(f'git checkout {destination_branch} || git checkout -b {destination_branch}', shell=True)

    os.makedirs(destination_directory, exist_ok=True)
    if clean:
        for path in glob(f'{destination_directory}/*'):
            if '.git/' not in path:
                remove_anything(path)

    subprocess.check_output(f'cp -r {source_directory}/* {destination_directory}', shell=True)
    push()


def get_current_branch_name():
    return os.environ['GITHUB_REF'].split('/')[-1]
