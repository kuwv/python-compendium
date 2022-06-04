# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
# type: ignore
"""Test YAML configuration management."""

import os
import pytest

from compendium.loader import ConfigFile
from compendium.exceptions import ConfigFileError

basedir = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(basedir, 'config.yaml')


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_filepath(fs):
    """Test YAML paths."""
    fs.add_real_file(filepath)
    cfg = ConfigFile(filepath=os.path.join(basedir, 'config.yaml'))
    assert f"{basedir}/config.yaml" == cfg.filepath


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_yaml_content(fs):
    """Test read YAML content."""
    fs.add_real_file(filepath)
    cfg = ConfigFile()
    settings = cfg.load(filepath=filepath)
    assert settings.retrieve('/stooges/stooge1') == 'Larry'
    assert settings.retrieve('/stooges/stooge2') == 'Curly'
    assert settings.retrieve('/stooges/stooge3') == 'Moe'
    assert settings.retrieve('/fruit') != 'banana'
    assert settings.retrieve('/number') == 2


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_yaml_content_dump(fs):
    """Test YAML content save."""
    fs.add_real_file(filepath, False)
    cfg = ConfigFile(writable=True)
    settings = cfg.load(filepath=filepath)
    settings.create('/test', 'test')
    assert settings['test'] == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    """Test YAML content fail."""
    fs.add_real_file(filepath)
    cfg = ConfigFile()
    settings = cfg.load(filepath=filepath)

    with pytest.raises(ConfigFileError):
        settings.create('/test', 'test')
        cfg.dump(settings, './config.yaml')
