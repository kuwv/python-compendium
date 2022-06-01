# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
# type: ignore
"""Test XML content management."""

import os

import pytest

from compendium.loader import ConfigFile
from compendium.exceptions import ConfigFileError

xmltodict = pytest.importorskip('xmltodict')

basedir = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(basedir, 'test.xml')


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_filepath(fs):
    """Test XML path."""
    fs.add_real_file(filepath)
    cfg = ConfigFile(
        name='tests',
        filepath=os.path.join(basedir, 'test.xml'),
    )
    assert f"{basedir}/test.xml" == cfg.filepath


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_xml_content(fs):
    """Test XML content read."""
    fs.add_real_file(filepath)
    cfg = ConfigFile(name='tests')
    cfg.load(filepath=filepath)
    assert settings.retrieve('/root/stooges/stooge1') == 'Larry'
    assert settings.retrieve('/root/stooges/stooge2') == 'Curly'
    assert settings.retrieve('/root/stooges/stooge3') == 'Moe'
    assert settings.retrieve('/root/fruit') != 'banana'
    assert settings.retrieve('/root/number') == '2'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_xml_content_dump(fs):
    """Test XML content save."""
    fs.add_real_file(filepath, False)
    cfg = ConfigFile(name='tests', writable=True)
    settings = cfg.load(filepath=filepath)
    settings.create('/root/test', 'test')
    assert settings.retrieve('/root/test') == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    """Test XML failure."""
    fs.add_real_file(filepath)
    cfg = ConfigFile(name='tests')
    settings = cfg.load(filepath=filepath)

    with pytest.raises(ConfigFileError):
        settings.create('/test', 'test')
        cfg.dump(settings, './test.xml')
