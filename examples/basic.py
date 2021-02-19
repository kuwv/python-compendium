# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Example YAML config.'''

import os

from compendium.config_manager import ConfigManager

filepath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'example.yaml'
)


cfg = ConfigManager(application='tests')
cfg.load(filepath=filepath)
print('settings', cfg.settings.__dict__)
# print('allowed_roles', cfg.settings.allowed_roles[0])
# print('default_args', cfg.settings.dag.default_args)
assert 'sre' in cfg.settings.get('/allowed_roles')
assert 'devops' in cfg.settings.get('/allowed_roles')
assert 'cloudops' in cfg.settings.get('/allowed_roles')
print('post settings', cfg.settings)
