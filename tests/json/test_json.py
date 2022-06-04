# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
# type: ignore
"""Test JSON content management."""

import os
import pytest

from compendium.loader import ConfigFile
from compendium.exceptions import ConfigFileError

basedir = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(basedir, 'config.json')


# @pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
# def test_empty_filepath(fs):
#     """Test empty file."""
#     cfg = ConfigPaths(name='empty')
#     cfg.load_configs(filename='config.json')
#     assert not cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_filepath(fs):
    """Test JSON filepaths."""
    fs.add_real_file(filepath)
    cfg = ConfigFile(filepath=os.path.join(basedir, 'config.json'))
    assert f"{basedir}/config.json" == cfg.filepath


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg(fs):
    """Test loading JSON configuration."""
    fs.add_real_file(filepath)
    cfg = ConfigFile()
    settings = cfg.load(filepath=filepath)
    assert settings.retrieve('/stooges/stooge1') == 'Larry'
    assert settings.retrieve('/stooges/stooge2') == 'Curly'
    assert settings.retrieve('/stooges/stooge3') == 'Moe'
    assert settings.retrieve('/fruit') != 'banana'
    assert settings.retrieve('/number') == 2


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_dump(fs):
    """Test saving JSON content."""
    fs.add_real_file(filepath, False)
    cfg = ConfigFile(writable=True)
    settings = cfg.load(filepath=filepath)
    settings.create('/test', 'test')
    assert settings.retrieve('test') == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    """Test JSON failure."""
    fs.add_real_file(filepath)
    cfg = ConfigFile()
    settings = cfg.load(filepath=filepath)

    with pytest.raises(ConfigFileError):
        settings.create('/test', 'test')
        cfg.dump(settings, './config.json')
