# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Example YAML config."""

import os

from compendium.config_manager import ConfigManager

print('------ example write for config_manager ------')

basedir = os.path.dirname(__file__)
filepath = os.path.join(basedir, 'example.yaml')
outpath = os.path.join(basedir, 'example-out.yaml')

cfg = ConfigManager(name='tests', writable=True)
cfg.load_config(filepath=filepath)

# print('settings', cfg)
assert 'sre' in cfg.retrieve('/allowed_roles')
assert 'devops' in cfg.retrieve('/allowed_roles')
assert 'cloudops' in cfg.retrieve('/allowed_roles')
assert cfg.retrieve('/dag/default_args/owner') == 'admin'

# print('post settings', cfg.data)
# cfg.dump_config(filepath=outpath)

print('------ example multi-file settings for config_manager ------')

filepaths = [
  os.path.join(basedir, 'config1.yaml'),
  os.path.join(basedir, 'config2.yaml'),
]

cfg_mgr = ConfigManager(filepaths=filepaths, separator='.')
version = cfg_mgr.lookup('.proman.version', '.tool.example.version')
print(version)
assert version == '1.2.3'
assert version != '1.2.4.dev0'
