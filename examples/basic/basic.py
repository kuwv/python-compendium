# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Example YAML config.'''

import os
from compendium.loader import ConfigFile


def show_types(obj):
    '''Recursively show dict types.'''
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

cfg = ConfigFile(name='tests')
cfg.load(filepath=filepath)

print('settings', cfg.settings.__dict__)
# print('allowed_roles', cfg.settings.allowed_roles[0])
# print('default_args', cfg.settings.dag.default_args)
# assert 'sre' in cfg.settings.get('/allowed_roles')
# assert 'devops' in cfg.settings.get('/allowed_roles')
# assert 'cloudops' in cfg.settings.get('/allowed_roles')

print('post settings', cfg.settings.data)
cfg.dump(filepath=outpath, writable=True)

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
json_cfg = ConfigFile(name='json')
json_cfg.load(filepath=json_in)
json_cfg.dump(filepath=json_out, writable=True)
json_cfg.dump(filepath=yaml_out, writable=True)
json_cfg.dump(filepath=toml_out, writable=True)

# YAML
yaml_cfg = ConfigFile(name='yaml')
yaml_cfg.load(filepath=yaml_in)
yaml_cfg.dump(filepath=yaml_out, writable=True)
yaml_cfg.dump(filepath=json_out, writable=True)
json_cfg.dump(filepath=toml_out, writable=True)

# TOML
toml_cfg = ConfigFile(name='toml')
toml_cfg.load(filepath=toml_in)
toml_cfg.dump(filepath=toml_out, writable=True)
toml_cfg.dump(filepath=json_out, writable=True)
toml_cfg.dump(filepath=yaml_out, writable=True)

print(show_types(json_cfg.settings.data))

print(show_types(toml_cfg.settings.data))

print(show_types(yaml_cfg.settings.data))

print('compare toml to yaml', toml_cfg.settings.data == yaml_cfg.settings.data)
print('compare json to toml', json_cfg.settings.data == toml_cfg.settings.data)
print('compare yaml to json', yaml_cfg.settings.data == json_cfg.settings.data)
