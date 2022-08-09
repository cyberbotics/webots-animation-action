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
import sys
import re
import yaml
from glob import glob


def get_world_info(world_path):
    """Returns dictionary with details about the given Webots world."""
    description = ''
    title = ''
    with open(world_path, 'r') as f:
        world_content = f.read()

        # Parse `title`
        title_expr = re.compile(r'title\s\"(.*?)\"', re.MULTILINE | re.DOTALL)
        title_re = re.findall(title_expr, world_content)
        if title_re:
            title = title_re[0]

        # Parse `info`
        info_expr = re.compile(r'info\s\[(.*?)\]', re.MULTILINE | re.DOTALL)
        info_re = re.findall(info_expr, world_content)
        if info_re:
            description = ' '.join([x.strip().strip('"') for x in info_re[0].split('\n') if x.strip().strip('"')])

    world_name = os.path.splitext(os.path.basename(world_path))[0]

    return {
        'title': title,
        'description': description,
        'name': world_name
    }


def expand_world_list(world_list):
    """
    Expands regex defined worlds.

    An example of the input config:
    ```
        [
            {"file": "worlds/*.wbt", "duration": 10}
        ]
    ```
    expands to:
    ```
        [
            {"file": "worlds/world_a.wbt", "duration": 10},
            {"file": "worlds/world_b.wbt", "duration": 10}
        ]
    ```
    """
    expanded_world_list = []
    for world_config in world_list:
        for world_file in glob(world_config['file']):
            new_world = world_config.copy()
            new_world['file'] = world_file
            expanded_world_list.append(new_world)
    return expanded_world_list


def compile_controllers(base='.'):
    for path in glob(os.path.join(base, 'controllers/*')):
        if os.path.isdir(path):
            if os.path.isfile(os.path.join(path, 'Makefile')):
                subprocess.check_output(f'cd {path} && make', shell=True)


def load_config(files=['webots.yaml', 'webots.yml']):
    """Load config from webots.yaml located in the repository root."""

    config = None
    for file in files:
      if os.path.isfile(file):
          with open(file, 'r') as f:
              config = yaml.load(f.read(), Loader=yaml.FullLoader) or {}
          break
    if config is None:
        print('Cannot load `webots.yaml`')
        sys.exit(1)
    return config
