# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Example YAML config."""

import os
from dataclasses import InitVar, dataclass, field
from typing import Any, Dict

from compendium.loader import ConfigFile


@dataclass
class Config(ConfigFile):
    """Manage settings from configuration file."""

    filepath: str
    writable: InitVar[bool] = True
    settings: Dict[str, Any] = field(init=False)

    def __post_init__(self, writable: bool) -> None:
        """Initialize settings from configuration."""
        super().__init__(self.filepath, writable=writable)
        self.settings = self.load()


basepath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(basepath, 'example.yaml')
outpath = os.path.join(basepath, 'example-out.yaml')

cfg = Config(filepath, writable=True)

print('settings', cfg.settings)
print('allowed_roles', cfg.settings.lookup('allowed_roles'))
assert 'sre' in cfg.settings.lookup('/allowed_roles')  # type: ignore
assert 'devops' in cfg.settings.lookup('/allowed_roles')  # type: ignore
assert 'cloudops' in cfg.settings.lookup('/allowed_roles')  # type: ignore

print('post settings', cfg.settings)
cfg.dump(cfg.settings.data, filepath=outpath)  # type: ignore
