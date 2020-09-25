#!/usr/bin/env python
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

from glob import glob
import yaml
import os
import re
import collections
from command import Command


def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    # Reference: https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
    for k in merge_dct.keys():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.abc.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


def load_config():
    default_config_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'config')

    # Load user's config
    user_config = {}
    if os.path.isfile('webots.yaml'):
        with open('webots.yaml', 'r') as f:
            user_config = yaml.load(f.read(), Loader=yaml.FullLoader) or {}

    # Load default config
    config = None
    with open(os.path.join(default_config_dir, 'webots.yaml'), 'r') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)

    # Put user's config on top of default config
    dict_merge(config, user_config)

    return config


def generate_animation_recorder_vrml(duration, output):
    return (
        f'Robot {{\n'
        f'  name "supervisor"\n'
        f'  controller "animation_recorder"\n'
        f'  controllerArgs [\n'
        f'      "--duration={duration}"\n'
        f'      "--output={output}"\n'
        f'  ]\n'
        f'  supervisor TRUE\n'
        f'}}\n'
    )


def get_world_name_from_path(path):
    return os.path.splitext(os.path.basename(path))[0]


def generate_animation_list(animation_config):
    template = None
    template_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(template_dir, 'template.html'), 'r') as f:
        template = f.read()

    worlds = []
    for world in animation_config['worlds']:
        for world_file in glob(world['file']):
            description = ''
            title = ''
            with open(world_file, 'r') as f:
                world_content = f.read()

                # Parse `title`
                title_expr = re.compile(
                    r'title\s\"(.*?)\"', re.MULTILINE | re.DOTALL)
                title_re = re.findall(title_expr, world_content)
                if title_re:
                    title = title_re[0]

                # Parse `info`
                info_expr = re.compile(
                    r'info\s\[(.*?)\]', re.MULTILINE | re.DOTALL)
                info_re = re.findall(info_expr, world_content)
                if info_re:
                    description = ' '.join(
                        [x.strip().strip('"') for x in info_re[0].split('\n') if x.strip().strip('"')]
                    )

            worlds.append({
                'title': title,
                'description': description,
                'name': get_world_name_from_path(world_file)
            })

    template = template.replace('{ WORLD_LIST_PLACEHOLDER }', str(worlds))

    with open(os.path.join('/tmp/animation', 'index.html'), 'w') as f:
        f.write(template)


def generate_animation(animation_config):
    generate_animation_list(animation_config)

    for world in animation_config['worlds']:
        for world_file in glob(world['file']):
            world_content = None
            world_name = get_world_name_from_path(world_file)
            animation_recorder_vrml = generate_animation_recorder_vrml(
                duration=world['duration'],
                output=os.path.join(os.path.abspath(
                    '.'), '/tmp/animation', world_name + '.html')
            )

            with open(world_file, 'r') as f:
                world_content = f.read()

            with open(world_file, 'w') as f:
                f.write(world_content + animation_recorder_vrml)

            command = Command(
                f"xvfb-run webots --stdout --stderr --batch --mode=fast {world_file}")
            command.run()

            with open(world_file, 'w') as f:
                f.write(world_content)


def main():
    config = load_config()
    generate_animation(config['animation'])


if __name__ == "__main__":
    main()
