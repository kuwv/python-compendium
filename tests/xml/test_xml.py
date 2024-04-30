# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
# type: ignore
"""Test XML content management."""

import os

import pytest

from compendium.exceptions import ConfigFileError
from compendium.loader import ConfigFile

xmltodict = pytest.importorskip('xmltodict')

basedir = os.path.dirname(__file__)
filepath = os.path.join(basedir, 'config.xml')


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_filepath(fs):
    """Test XML path."""
    fs.add_real_file(filepath)
    cfg = ConfigFile(filepath=os.path.join(basedir, 'config.xml'))
    assert f"{basedir}/config.xml" == cfg.filepath


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_xml_content(fs):
    """Test XML content read."""
    fs.add_real_file(filepath)
    cfg = ConfigFile()
    settings = cfg.load(filepath=filepath)
    assert settings['/root/stooges/stooge1'] == 'Larry'
    assert settings['/root/stooges/stooge2'] == 'Curly'
    assert settings['/root/stooges/stooge3'] == 'Moe'
    assert settings['/root/fruit'] != 'banana'
    assert settings['/root/number'] == '2'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_xml_content_dump(fs):
    """Test XML content save."""
    fs.add_real_file(filepath, False)
    cfg = ConfigFile(writable=True)
    settings = cfg.load(filepath=filepath)
    settings['/root/test'] = 'test'
    assert settings['/root/test'] == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    """Test XML failure."""
    fs.add_real_file(filepath)
    cfg = ConfigFile()
    settings = cfg.load(filepath=filepath)

    with pytest.raises(ConfigFileError):
        settings['/test'] = 'test'
        cfg.dump(settings, './config.xml')
