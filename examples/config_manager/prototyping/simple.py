# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Example YAML config."""

import logging
import os
from collections import ChainMap
from typing import Any, Dict, Mapping, Optional

from dpath import util as dpath
from dpath.exceptions import PathNotFound

from compendium import ConfigManager, SettingsMap

log = logging.getLogger(__name__)


if __name__ == '__main__':
    basedir = os.path.dirname(__file__)
    filepaths = [
      os.path.join(basedir, 'config1.toml'),
      os.path.join(basedir, 'config2.toml'),
    ]

    cfg_mgr = ConfigManager(filepaths=filepaths, separator='.')
    assert cfg_mgr.separator == cfg_mgr.data.separator

    version = cfg_mgr.lookup('project.version', 'tool.example.version')
    assert version == '1.2.3'
    assert version != '1.2.4.dev0'
