import subprocess
import os
import re
from glob import glob
import requests


def is_debug():
    return 'DEBUG' in os.environ and os.environ['DEBUG']


def install_dependencies(init):
    out = subprocess.check_output(init, shell=True)
    print(out.decode('utf-8'))


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


def _configure_git():
    username = os.environ['GITHUB_ACTOR']
    user_info = requests.get(f'https://api.github.com/users/{username}').json()

    result = subprocess.run('git config --list | grep user.name', shell=True, check=False)
    if result.returncode != 0:
        email = '${}+${}@users.noreply.github.com'.format(user_info['id'], username)
        subprocess.check_output(['git', 'config', '--global', 'user.name', user_info['name']])
        subprocess.check_output(['git', 'config', '--global', 'user.email', email])


def git_push(message='Updated animation'):
    _configure_git()

    github_repository = 'https://{}:{}@github.com/{}'.format(
        os.environ['GITHUB_ACTOR'],
        os.environ['GITHUB_TOKEN'],
        os.environ['GITHUB_REPOSITORY']
    )

    subprocess.check_output(['git', 'add', '-A'])
    subprocess.check_output(['git', 'commit', '-m', message])
    if not is_debug():
        subprocess.check_output(['git', 'push', github_repository])
    else:
        print(f'@ git push {github_repository}')


def git_push_directory_to_branch(source_directory, destination_directory='.', destination_branch='gh-pages', clean=False):
    """Publishes an arbitrary dictionary to a new branch (usually `gh-pages`)."""

    _configure_git()

    subprocess.check_output(['git', 'reset', '--hard'])
    subprocess.check_output(['git', 'fetch'])
    subprocess.check_output(f'git checkout {destination_branch} || git checkout -b {destination_branch}', shell=True)

    os.makedirs(destination_directory, exist_ok=True)
    if clean:
        subprocess.check_output(['rm', '-rf', f'{destination_directory}/*'])

    subprocess.check_output(f'cp -r {source_directory}/* {destination_directory}', shell=True)
    git_push()


def compile_controllers():
    for path in glob('controllers/*'):
        if os.path.isdir(path):
            if os.path.isfile(os.path.join(path, 'Makefile')):
                subprocess.check_output(f'cd {path} && make', shell=True)
