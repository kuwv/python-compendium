# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Example YAML config."""

import os

from compendium.config_manager import ConfigManager
from compendium.loader import ConfigFile

basedir = os.path.dirname(__file__)
filepath = os.path.join(basedir, 'example.yaml')
outpath = os.path.join(basedir, 'example-out.yaml')

cfg = ConfigManager(name='tests', writable=True)
cfg.load_config(config_file=ConfigFile(filepath))

# print('settings', cfg)
assert 'sre' in cfg['/allowed_roles']
assert 'devops' in cfg['/allowed_roles']
assert 'cloudops' in cfg['/allowed_roles']
assert cfg['/dag/default_args/owner'] == 'admin'

# print('post settings', cfg)
# cfg.dump_config(filepath=outpath)
