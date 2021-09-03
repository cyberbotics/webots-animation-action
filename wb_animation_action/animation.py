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
import sys
import shutil
from glob import glob
import subprocess
from wb_animation_action.config import RESOURCES_DIRECTORY
import wb_animation_action.utils.git
from wb_animation_action.utils.git import get_current_branch_name
from wb_animation_action.utils.webots import get_world_info, expand_world_list, compile_controllers


def _generate_animation_recorder_vrml(duration, output):
    return (
        f'Robot {{\n'
        f'  name "supervisor"\n'
        f'  controller "animation_recorder"\n'
        f'  controllerArgs [\n'
        f'    "--duration={duration}"\n'
        f'    "--output={output}"\n'
        f'  ]\n'
        f'  children [\n'
        f'    Receiver {{\n'
        f'      channel 1024\n'
        f'    }}\n'
        f'  ]\n'
        f'  supervisor TRUE\n'
        f'}}\n'
    )


def _get_animation_directories():
    directories = []
    for path in glob('*'):
        if os.path.isdir(path) and os.path.isfile(os.path.join(path, 'index.html')):
            directories.append(path)
    return directories


def _generate_animation_page(worlds_config):
    template = None

    # Generate details
    worlds = [get_world_info(world_config['file']) for world_config in worlds_config]

    # Write to the template
    with open(os.path.join(RESOURCES_DIRECTORY, 'animation-page.template.html'), 'r') as f:
        template = f.read()
    template = template.replace('{ WORLD_LIST_PLACEHOLDER }', str(worlds))
    with open(os.path.join('/tmp/animation', 'index.html'), 'w') as f:
        f.write(template)


def _generate_branch_index():
    with open(os.path.join(RESOURCES_DIRECTORY, 'animation-list.template.html'), 'r') as f:
        template = f.read()
    worlds = [f'<li><a href="{path}">{path}</a></li>' for path in _get_animation_directories()]
    template = template.replace('{ BRANCH_LIST_PLACEHOLDER }', '\n'.join(worlds))
    with open('index.html', 'w') as f:
        f.write(template)
    wb_animation_action.utils.git.push()


def generate_animation_for_world(world_file, duration, destination_directory='/tmp/animation'):
    """Generates animation for world given by `world_file`."""

    world_info = get_world_info(world_file)

    # Append `animation_recorder` controller
    animation_recorder_vrml = _generate_animation_recorder_vrml(
        duration=duration,
        output=os.path.join(os.path.abspath('.'), destination_directory, world_info['name'] + '.html')
    )
    with open(world_file, 'r') as f:
        world_content = f.read()
    with open(world_file, 'w') as f:
        f.write(world_content + animation_recorder_vrml)
    subprocess.check_output(['mkdir', '-p', destination_directory])

    # Runs simulation in Webots
    out = subprocess.Popen(
        ['xvfb-run', 'webots', '--stdout', '--stderr', '--batch', '--mode=fast', '--no-rendering', world_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    while not out.poll():
        stdoutdata = out.stdout.readline()
        if stdoutdata:
            print(stdoutdata.decode('utf-8'))
        else:
            break

    # Removes `animation_recorder` controller
    with open(world_file, 'w') as f:
        f.write(world_content)


def generate_animation(animation_config):
    """Generates animation for all worlds based on the given content."""

    # Add default config
    if 'worlds' not in animation_config:
        animation_config['worlds'] = {
            'file': 'worlds/*.wbt',
            'duration': 10
        }

    # Expand world list (handle regex expressions)
    animation_config['worlds'] = expand_world_list(animation_config['worlds'])

    # Generate animation for each world
    compile_controllers()
    for world_config in animation_config['worlds']:
        generate_animation_for_world(world_config['file'], world_config['duration'])

    # Generates list of animations
    _generate_animation_page(animation_config['worlds'])

    # Push animation to gh-pages
    current_branch_name = get_current_branch_name()
    wb_animation_action.utils.git.push_directory_to_branch(
        '/tmp/animation',
        destination_directory=current_branch_name,
        clean=True
    )

    # Update branch index list (we assume we are in `gh-pages` branch)
    _generate_branch_index()
    
    # Delete files that are not necessary
    animation_directories = _get_animation_directories()
    for path in glob('*'):
        if path not in _get_animation_directories() + ['index.html']:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
