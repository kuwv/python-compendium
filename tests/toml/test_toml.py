# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
# type: ignore
"""Test TOML configuration management."""

import os
import pytest

from compendium.loader import ConfigFile
from compendium.exceptions import ConfigFileError

basedir = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(basedir, 'test.toml')


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_filepath(fs):
    """Test TOML filepaths."""
    fs.add_real_file(filepath)
    cfg = ConfigFile(
        name='toml',
        filepath=os.path.join(basedir, 'test.toml')
    )
    assert f"{basedir}/test.toml" == cfg.filepath


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content(fs):
    """Test TOML content load."""
    fs.add_real_file(filepath)
    cfg = ConfigFile(name='tests')
    settings = cfg.load(filepath=filepath)
    assert settings.retrieve('/stooges/stooge1') == 'Larry'
    assert settings.retrieve('/stooges/stooge2') == 'Curly'
    assert settings.retrieve('/stooges/stooge3') == 'Moe'
    assert settings.retrieve('/fruit') != 'banana'
    assert settings.retrieve('/number') == 2


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content_dump(fs):
    """Test TOML content save."""
    fs.add_real_file(filepath, False)
    cfg = ConfigFile(name='tests', writable=True)
    settings = cfg.load(filepath=filepath)
    settings.create('/test', 'test')
    # TODO where is save happening :/
    assert settings.retrieve('test') == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    """Test TOML content failure."""
    fs.add_real_file(filepath)
    cfg = ConfigFile(name='tests')
    settings = cfg.load(filepath=filepath)

    with pytest.raises(ConfigFileError):
        settings.create('/test', 'test')
        cfg.dump(settings, './test.toml')
