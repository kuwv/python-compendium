# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
# type: ignore
"""Test TOML configuration management."""

import os

import pytest

from compendium.exceptions import ConfigFileError
from compendium.loader import ConfigFile

basedir = os.path.dirname(__file__)
filepath = os.path.join(basedir, 'config.ini')


# def test_empty_filepath():
#     """Test empty file."""
#     cfg = ConfigFile(filename='config.ini')
#     cfg.load()
#     assert not cfg.filepath


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_filepath(fs):
    """Test TOML filepaths."""
    fs.add_real_file(filepath)
    cfg = ConfigFile(filepath=os.path.join(basedir, 'config.ini'))
    assert f"{basedir}/config.ini" == cfg.filepath


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_ini_content(fs):
    """Test TOML content load."""
    fs.add_real_file(filepath)
    cfg = ConfigFile()
    settings = cfg.load(filepath=filepath)
    assert settings['/stooges/stooge1'] == 'Larry'
    assert settings['/stooges/stooge2'] == 'Curly'
    assert settings['/stooges/stooge3'] == 'Moe'
    assert settings['/fruit'] == 'apple'
    assert int(settings['/number']) == 2


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_ini_content_dump(fs):
    """Test TOML content save."""
    fs.add_real_file(filepath, False)
    cfg = ConfigFile(writable=True)
    settings = cfg.load(filepath=filepath)
    settings['/test'] = 'test'
    # TODO where is save happening :/
    assert settings['test'] == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    """Test TOML content failure."""
    fs.add_real_file(filepath)
    cfg = ConfigFile()
    settings = cfg.load(filepath=filepath)

    with pytest.raises(ConfigFileError):
        settings['/test'] = 'test'
        cfg.dump(settings, './config.ini')
