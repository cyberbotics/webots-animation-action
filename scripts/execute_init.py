import os
import subprocess
import yaml

if os.path.isfile('webots.yaml'):
    with open('webots.yaml', 'r') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader) or {}
        out = subprocess.check_output(config['init'], shell=True)
        print(out.decode('utf-8'))
