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
settings = cfg.load(filepath=filepath)

print('settings', settings)
# print('allowed_roles', settings.allowed_roles[0])
# print('default_args', settings.dag.default_args)
# assert 'sre' in settings.get('/allowed_roles')
# assert 'devops' in settings.get('/allowed_roles')
# assert 'cloudops' in settings.get('/allowed_roles')

print('post settings', settings.data)
cfg.dump(settings.data, filepath=outpath)

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
json_cfg = ConfigFile(writable=True)
json_settings = json_cfg.load(filepath=json_in)
json_cfg.dump(json_settings.data, filepath=json_out)
json_cfg.dump(json_settings.data, filepath=yaml_out)
json_cfg.dump(json_settings.data, filepath=toml_out)

# YAML
yaml_cfg = ConfigFile(writable=True)
yaml_settings = yaml_cfg.load(filepath=yaml_in)
yaml_cfg.dump(yaml_settings.data, filepath=yaml_out)
yaml_cfg.dump(yaml_settings.data, filepath=json_out)
json_cfg.dump(yaml_settings.data, filepath=toml_out)

# TOML
toml_cfg = ConfigFile(writable=True)
toml_settings = toml_cfg.load(filepath=toml_in)
toml_cfg.dump(toml_settings.data, filepath=toml_out)
toml_cfg.dump(toml_settings.data, filepath=json_out)
toml_cfg.dump(toml_settings.data, filepath=yaml_out)

print(show_types(json_settings.data))
print(show_types(toml_settings.data))
print(show_types(yaml_settings.data))

print('compare toml to yaml', toml_settings.data == yaml_settings.data)
print('compare json to toml', json_settings.data == toml_settings.data)
print('compare yaml to json', yaml_settings.data == json_settings.data)
