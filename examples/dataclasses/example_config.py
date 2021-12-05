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
        super().__init__(self.filepath, writable=self.writable)
        self.load()


basepath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(basepath, 'example.yaml')
outpath = os.path.join(basepath, 'example-out.yaml')

cfg = Config(filepath, writable=True)

print('settings', cfg)
assert 'sre' in cfg.retrieve('/allowed_roles')  # type: ignore
assert 'devops' in cfg.retrieve('/allowed_roles')  # type: ignore
assert 'cloudops' in cfg.retrieve('/allowed_roles')  # type: ignore

print('post settings', cfg.data)
cfg.dump(filepath=outpath)
