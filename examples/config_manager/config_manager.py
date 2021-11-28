# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Example YAML config."""

import os

from compendium.config_manager import ConfigManager

basepath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(basepath, 'example.yaml')
outpath = os.path.join(basepath, 'example-out.yaml')

cfg = ConfigManager(name='tests', writable=True)
cfg.load_config(filepath=filepath)

# print('settings', cfg)
assert 'sre' in cfg.retrieve('/allowed_roles')
assert 'devops' in cfg.retrieve('/allowed_roles')
assert 'cloudops' in cfg.retrieve('/allowed_roles')
assert cfg.retrieve('/dag/default_args/owner') == 'admin'

print('post settings', cfg.data)
# cfg.dump_config(filepath=outpath)
