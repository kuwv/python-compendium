# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Example YAML config."""

from __future__ import annotations

import os
from collections.abc import MutableMapping
from dataclasses import InitVar, dataclass, field
from typing import Any

from compendium.loader import ConfigFile


@dataclass
class Config(ConfigFile):
    """Manage settings from configuration file."""

    filepath: str
    writable: InitVar[bool] = True
    settings: MutableMapping = field(init=False)

    def __post_init__(self, writable: bool) -> None:
        """Initialize settings from configuration."""
        super().__init__(self.filepath, writable=writable)
        self.settings = self.load()


BASEPATH = os.path.dirname(os.path.realpath(__file__))
INPATH = os.path.join(BASEPATH, 'example.yaml')
OUTPATH = os.path.join(BASEPATH, 'example-out.yaml')

cfg = Config(INPATH, writable=True)

print('settings', cfg.settings)
print('allowed_roles', cfg.settings.get('allowed_roles'))
assert 'sre' in cfg.settings.get('/allowed_roles', [])
assert 'devops' in cfg.settings.get('/allowed_roles', [])
assert 'cloudops' in cfg.settings.get('/allowed_roles', [])

# XXX: need generic compendium.Settings[K, V]
print('post settings', cfg.settings)
if hasattr(cfg.settings, 'data'):
    cfg.dump(cfg.settings.data, filepath=OUTPATH)
else:
    raise AttributeError(
        'provided factory type of Config does not support data attribute'
    )
