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
    with ConfigFile(os.path.join(basedir, 'config.xml')) as cfg:
        assert os.path.join(basedir, 'config.xml') == cfg.filepath


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_xml_content(fs):
    """Test XML content read."""
    fs.add_real_file(filepath)
    with ConfigFile(filepath) as cfg:
        assert cfg.settings['/root/stooges/stooge1'] == 'Larry'
        assert cfg.settings['/root/stooges/stooge2'] == 'Curly'
        assert cfg.settings['/root/stooges/stooge3'] == 'Moe'
        assert cfg.settings['/root/fruit'] != 'banana'
        assert cfg.settings['/root/number'] == '2'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_xml_content_dump(fs):
    """Test XML content save."""
    fs.add_real_file(filepath, False)
    with ConfigFile(filepath, writable=True) as cfg:
        cfg.settings['/root/test'] = 'test'
        assert cfg.settings['/root/test'] == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    """Test XML failure."""
    fs.add_real_file(filepath)
    with ConfigFile(filepath, writable=False) as cfg:
        with pytest.raises(ConfigFileError):
            cfg.settings['/test'] = 'test'
            cfg.dump(cfg.settings)
