# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
# type: ignore
"""Test YAML configuration management."""

import os

import pytest

from compendium.exceptions import ConfigFileError
from compendium.loader import ConfigFile

basedir = os.path.dirname(__file__)
filepath = os.path.join(basedir, 'config.yaml')


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_filepath(fs):
    """Test YAML paths."""
    fs.add_real_file(filepath)
    cfg = ConfigFile(os.path.join(basedir, 'config.yaml'))
    assert os.path.join(basedir, 'config.yaml') == cfg.filepath


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_yaml_content(fs):
    """Test read YAML content."""
    fs.add_real_file(filepath)
    cfg = ConfigFile(filepath)
    settings = cfg.load()
    assert settings['/stooges/stooge1'] == 'Larry'
    assert settings['/stooges/stooge2'] == 'Curly'
    assert settings['/stooges/stooge3'] == 'Moe'
    assert settings['/fruit'] != 'banana'
    assert settings['/number'] == 2


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_yaml_content_dump(fs):
    """Test YAML content save."""
    fs.add_real_file(filepath, False)
    cfg = ConfigFile(filepath, writable=True)
    settings = cfg.load()
    settings['/test'] = 'test'
    assert settings['test'] == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    """Test YAML content fail."""
    fs.add_real_file(filepath)
    cfg = ConfigFile(filepath)
    settings = cfg.load()

    with pytest.raises(ConfigFileError):
        settings['/test'] = 'test'
        cfg.dump(settings, './config.yaml')
