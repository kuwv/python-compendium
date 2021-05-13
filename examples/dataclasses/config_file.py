# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Example YAML config.'''

import os
from dataclasses import dataclass

from compendium.loader import ConfigFile


@dataclass
class Config(ConfigFile):
    '''Manage settings from configuration file.'''

    filepath: str
    writable: bool = True

    def __post_init__(self) -> None:
        '''Initialize settings from configuration.'''
        super().__init__(self.filepath)
        self.load()


basepath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(basepath, 'example.yaml')
outpath = os.path.join(basepath, 'example-out.yaml')

cfg = Config(filepath)

print('settings', cfg)
# print('allowed_roles', cfg.allowed_roles[0])
# print('default_args', cfg.dag.default_args)
# assert 'sre' in cfg.get('/allowed_roles')
# assert 'devops' in cfg.get('/allowed_roles')
# assert 'cloudops' in cfg.get('/allowed_roles')

print('post settings', cfg.data)
cfg.dump(filepath=outpath, writable=True)
