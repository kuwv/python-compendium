# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Example YAML config."""

import os

from compendium.config_manager import ConfigManager

if __name__ == '__main__':
    basedir = os.path.dirname(__file__)
    filepaths = [
        os.path.join(basedir, 'config1.toml'),
        os.path.join(basedir, 'config2.toml'),
    ]

    cfg = ConfigManager(filepaths=filepaths, separator='.')
    assert cfg.separator == '.'
    assert cfg.data.separator == '.'

    version = cfg.lookup('project.version', 'tool.example.version')
    assert version == '1.2.3'
    assert version != '1.2.4.dev0'
