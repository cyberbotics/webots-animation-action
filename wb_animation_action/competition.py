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
import wb_animation_action.utils
from wb_animation_action.animation import generate_animation_for_world
from wb_animation_action.utils.webots import compile_controllers


MATCH_TIMEOUT = 15 * 60


class Competitor:
    def __init__(self, git, rank, controller_name=None):
        self.git = git
        self.rank = rank
        if controller_name is None: 
            self.controller_name = self.__get_controller_name()
        else:
            self.controller_name = controller_name

    def __get_id(self):
        return re.findall(r'([^@:\/\.]*?)\/([^@:\/\.]*)', self.git)[0]

    def __get_controller_name(self):
        chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
        hash_string = ''.join(random.choice(chars) for _ in range(5))
        username, repository = self.__get_id()
        return f'wb_{username}_{repository}_{hash_string}'

    def get_dict(self):
        return {'git': self.git, 'rank': self.rank}

    def __str__(self):
        return self.__get_id()


def _get_competitors():
    competitors = []
    competitors.append(
        Competitor(
            git=None,
            rank=0,
            controller_name='dummy'
        )
    )
    with open('competitors.txt', 'r') as f:
        for rank, competitor_url in enumerate(f.readlines()):
            competitors.append(
                Competitor(
                    git=competitor_url,
                    rank=rank+1
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
            subprocess.check_output(f"git clone {competitor.git} {controller_path}", shell=True)

            # Update controller's internal name
            python_filename = os.path.join(controller_path, 'participant_controller.py')
            if os.path.exists(python_filename):
                os.rename(python_filename, os.path.join(controller_path, f'{competitor.controller_name}.py'))


def generate_competition(competition_config):
    world_file = competition_config['world']
    competitors = _get_competitors()
    matches = []

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
        generate_animation_for_world(world_file, MATCH_TIMEOUT, destination_directory=destination_directory)

        # Update ranks
        winner = None
        with open('/tmp/winner.txt', 'r') as f:
            winner = f.read()
        if winner == 1:
            competitor_a.rank -= 1
            competitor_b.rank += 1
            competitors = sorted(competitors, lambda c: c.rank)
        
        # Store the results
        matches.append({
            'directory': match_directory,
            'competitor_a': str(competitor_a),
            'competitor_b': str(competitor_b),
            'winner': 'competitor_b' if winner == 1 else 'competitor_a'
        })

        # Prepare next iteration
        lower_competitor_index -= 1

    # Write animation
    wb_animation_action.utils.git.push_directory_to_branch('/tmp/animation', clean=True)

    # Write results
    os.makedirs('/tmp/results', exist_ok=True)
    results = {
        'ranking': [c.get_dict() for c in competitors],
        'matches': matches
    }
    with open(os.path.join('/tmp/results', 'results.json'), 'w') as f:
        f.write(json.dumps(results))
    wb_animation_action.utils.git.push_directory_to_branch('/tmp/results')
