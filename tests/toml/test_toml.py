# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
# type: ignore
"""Test TOML configuration management."""

import os

import pytest

from compendium.exceptions import ConfigFileError
from compendium.loader import ConfigFile

basedir = os.path.dirname(__file__)
filepath = os.path.join(basedir, 'config.toml')


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_filepath(fs):
    """Test TOML filepaths."""
    fs.add_real_file(filepath)
    with ConfigFile(os.path.join(basedir, 'config.toml')) as cfg:
        assert os.path.join(basedir, 'config.toml') == cfg.filepath


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content(fs):
    """Test TOML content load."""
    fs.add_real_file(filepath)
    with ConfigFile(filepath) as cfg:
        assert cfg.settings['/stooges/stooge1'] == 'Larry'
        assert cfg.settings['/stooges/stooge2'] == 'Curly'
        assert cfg.settings['/stooges/stooge3'] == 'Moe'
        assert cfg.settings['/fruit'] != 'banana'
        assert cfg.settings['/number'] == 2


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content_dump(fs):
    """Test TOML content save."""
    fs.add_real_file(filepath, False)
    with ConfigFile(filepath, writable=True) as cfg:
        cfg.settings['/test'] = 'test'
        assert cfg.settings['test'] == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    """Test TOML content failure."""
    fs.add_real_file(filepath)
    with ConfigFile(filepath, writable=False) as cfg:
        with pytest.raises(ConfigFileError):
            cfg.settings['/test'] = 'test'
            cfg.dump(cfg.settings)
