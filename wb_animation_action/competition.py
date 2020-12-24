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

import re
import os
import json
import random
import string
import subprocess
from glob import glob
from shutil import copyfile
import wb_animation_action.utils
from distutils.dir_util import copy_tree
from wb_animation_action.config import COMPETITION_TIMEOUT, RESOURCES_DIRECTORY, ADD_DUMMY_TO_COMPETITION
from wb_animation_action.animation import generate_animation_for_world
from wb_animation_action.utils.webots import compile_controllers
from wb_animation_action.utils.github import accept_all_invitations


class Competitor:
    def __init__(self, git, rank, controller_name=None):
        self.git = git
        self.rank = rank
        self.username = None
        self.repository_name = None
        self.controller_name = None
        if self.git:
            self.username, self.repository_name = re.findall(
                r'github\.com\/([a-zA-Z0-9\-\_]*)\/([a-zA-Z0-9\-\_]*)', self.git
            )[0]
        if controller_name is None:
            self.controller_name = self.__get_controller_name()
        else:
            self.controller_name = controller_name

    def __get_id(self):
        if self.username and self.repository_name:
            return f'{self.username}_{self.repository_name}'
        return 'dummy'

    def __get_controller_name(self):
        chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
        hash_string = ''.join(random.choice(chars) for _ in range(5))
        return f'wb_{self.__get_id()}_{hash_string}'

    def get_dict(self):
        return {
            'id': self.__get_id(),
            'rank': self.rank,
            'username': self.username,
            'repository_name': self.repository_name
        }

    def __str__(self):
        return self.__get_id()


def _get_competitors():
    competitors = []
    rank_start = 1
    if ADD_DUMMY_TO_COMPETITION:
        competitors.append(
            Competitor(
                git=None,
                rank=rank_start,
                controller_name='dummy'
            )
        )
        rank_start += 1
    with open('competitors.txt', 'r') as f:
        for rank, competitor_url in enumerate(f.readlines()):
            competitors.append(
                Competitor(
                    git=competitor_url.strip(),
                    rank=rank+rank_start
                )
            )
    return competitors


def _set_controller_name_to_world(world_file, robot_name, controller_name):
    world_content = None
    with open(world_file, 'r') as f:
        world_content = f.read()
    controller_expression = re.compile(rf'(DEF {robot_name}.*?controller\ \")(.*?)(\")', re.MULTILINE | re.DOTALL)
    new_world_content = re.sub(controller_expression, rf'\1{controller_name}\3', world_content)
    with open(world_file, 'w') as f:
        f.write(new_world_content)


def _clone_controllers(competitors):
    # Clone controller content
    for competitor in competitors:
        if competitor.git is not None:
            controller_path = os.path.join('controllers', competitor.controller_name)
            repo = 'https://{}:{}@github.com/{}/{}'.format(
                os.environ['BOT_USERNAME'],
                os.environ['BOT_PAT_KEY'],
                competitor.username,
                competitor.repository_name
            )
            subprocess.check_output(f'git clone {repo} {controller_path}', shell=True)

            # Update controller's internal name (Python)
            python_filename = os.path.join(controller_path, 'participant_controller.py')
            if os.path.exists(python_filename):
                os.rename(python_filename, os.path.join(controller_path, f'{competitor.controller_name}.py'))


def generate_competition(competition_config):
    world_file = competition_config['world']
    competitors = _get_competitors()
    matches = []

    # Accept all invitations
    accept_all_invitations(os.environ['BOT_PAT_KEY'])

    # Prepare directories
    os.makedirs('/tmp/output', exist_ok=True)

    # Prepare controllers
    _clone_controllers(competitors)
    compile_controllers()

    lower_competitor_index = len(competitors) - 1
    while lower_competitor_index > 0:
        competitor_a = competitors[lower_competitor_index - 1]
        competitor_b = competitors[lower_competitor_index]

        # Add two participants to the world
        _set_controller_name_to_world(world_file, 'R0', competitor_a.controller_name)
        _set_controller_name_to_world(world_file, 'R1', competitor_b.controller_name)

        # Run match
        match_directory = f'{competitor_a.controller_name}_vs_{competitor_b.controller_name}'
        destination_directory = os.path.join(
            '/tmp',
            'animation',
            match_directory
        )
        generate_animation_for_world(world_file, COMPETITION_TIMEOUT, destination_directory=destination_directory)

        json_file = glob(os.path.join(destination_directory, '*.json')).pop()
        os.rename(json_file, os.path.join(destination_directory, match_directory + '.json'))
        x3d_file = glob(os.path.join(destination_directory, '*.x3d')).pop()
        os.rename(x3d_file, os.path.join(destination_directory, 'model.x3d'))
        html_file = glob(os.path.join(destination_directory, '*.html')).pop()
        os.remove(html_file)
        copy_tree(destination_directory, '/tmp/output')

        # Update ranks
        winner = None
        points = []
        with open('/tmp/results.txt', 'r') as f:
            for line in f.readlines():
                pair = line.split(':')
                if len(pair) != 2 or line.startswith('#'):
                    continue
                key, value = pair
                if key == 'winner':
                    winner = int(value)
                elif key == 'points':
                    points = [float(x) for x in value.split(',')]

        if winner == 1:
            competitor_a.rank, competitor_b.rank = competitor_b.rank, competitor_a.rank
            competitors = sorted(competitors, key=lambda c: c.rank)

        # Store the results
        matches.append({
            'id': match_directory,
            'competitor_a': str(competitor_a),
            'competitor_b': str(competitor_b),
            'winner': 'competitor_b' if winner == 1 else 'competitor_a',
            'points': points
        })

        # Prepare next iteration
        lower_competitor_index -= 1

    # Write animation
    wb_animation_action.utils.git.push_directory_to_branch('/tmp/output', clean=True)

    # Write results
    os.makedirs('/tmp/results', exist_ok=True)
    results = {
        'ranking': [c.get_dict() for c in competitors],
        'matches': matches
    }
    with open(os.path.join('/tmp/results', 'results.json'), 'w') as f:
        f.write(json.dumps(results))
    copyfile(os.path.join(RESOURCES_DIRECTORY, 'competition.html'), '/tmp/results/index.html')
    wb_animation_action.utils.git.push_directory_to_branch('/tmp/results')
