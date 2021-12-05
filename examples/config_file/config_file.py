# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
# type: ignore
"""Example YAML config."""

import os
from compendium.loader import ConfigFile


def show_types(obj):
    """Recursively show dict types."""
    # convert associative array
    if isinstance(obj, dict):
        obj = {
            f"{type(str(k))}:{str(k)}": show_types(v)
            for k, v in obj.items()
        }

    # convert list
    elif isinstance(obj, list):
        obj = [show_types(x) for x in obj]

    return f"{type(obj)}:{obj}"


basepath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(basepath, 'example.yaml')
outpath = os.path.join(basepath, 'example-out.yaml')

cfg = ConfigFile(writable=True)
cfg.load(filepath=filepath)

print('settings', cfg)
# print('allowed_roles', cfg.allowed_roles[0])
# print('default_args', cfg.dag.default_args)
# assert 'sre' in cfg.get('/allowed_roles')
# assert 'devops' in cfg.get('/allowed_roles')
# assert 'cloudops' in cfg.get('/allowed_roles')

print('post settings', cfg.data)
cfg.dump(filepath=outpath)

# JSON
json_in = os.path.join(basepath, 'in.json')
json_out = os.path.join(basepath, 'out.json')

# YAML
yaml_in = os.path.join(basepath, 'in.yaml')
yaml_out = os.path.join(basepath, 'out.yaml')

# TOML
toml_in = os.path.join(basepath, 'in.toml')
toml_out = os.path.join(basepath, 'out.toml')

# JSON
json_cfg = ConfigFile(name='json', writable=True)
json_cfg.load(filepath=json_in)
json_cfg.dump(filepath=json_out)
json_cfg.dump(filepath=yaml_out)
json_cfg.dump(filepath=toml_out)

# YAML
yaml_cfg = ConfigFile(name='yaml', writable=True)
yaml_cfg.load(filepath=yaml_in)
yaml_cfg.dump(filepath=yaml_out)
yaml_cfg.dump(filepath=json_out)
json_cfg.dump(filepath=toml_out)

# TOML
toml_cfg = ConfigFile(name='toml', writable=True)
toml_cfg.load(filepath=toml_in)
toml_cfg.dump(filepath=toml_out)
toml_cfg.dump(filepath=json_out)
toml_cfg.dump(filepath=yaml_out)

print(show_types(json_cfg.data))

print(show_types(toml_cfg.data))

print(show_types(yaml_cfg.data))

print('compare toml to yaml', toml_cfg.data == yaml_cfg.data)
print('compare json to toml', json_cfg.data == toml_cfg.data)
print('compare yaml to json', yaml_cfg.data == json_cfg.data)
