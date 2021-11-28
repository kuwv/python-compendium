# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Test XML content management."""

import os
import pytest  # type: ignore

from compendium.loader import ConfigFile
from compendium.exceptions import CompendiumConfigFileError

config_filepath = os.path.dirname(os.path.realpath(__file__))
xml_filepath = os.path.join(config_filepath, 'test.xml')


# def test_empty_filepath():
#     """Test XML filepth."""
#     cfg = ConfigPaths(name='empty')
#     cfg.load_configs(filename='test.xml')
#     assert not cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_xml_filepath(fs):
    """Test XML path."""
    fs.add_real_file(xml_filepath)
    cfg = ConfigFile(
        name='tests',
        filepath=os.path.join(config_filepath, 'test.xml'),
    )
    assert "{}/test.xml".format(config_filepath) == cfg.filepath


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_xml_content(fs):
    """Test XML content read."""
    fs.add_real_file(xml_filepath)
    cfg = ConfigFile(name='tests')
    cfg.load(filepath=xml_filepath)
    assert cfg.retrieve('/root/stooges/stooge1') == 'Larry'
    assert cfg.retrieve('/root/stooges/stooge2') == 'Curly'
    assert cfg.retrieve('/root/stooges/stooge3') == 'Moe'
    assert cfg.retrieve('/root/fruit') != 'banana'
    assert cfg.retrieve('/root/number') == '2'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_xml_content_dump(fs):
    """Test XML content save."""
    fs.add_real_file(xml_filepath, False)
    cfg = ConfigFile(name='tests', writable=True)
    cfg.load(filepath=xml_filepath)
    cfg.create('/root/test', 'test')
    assert cfg.retrieve('/root/test') == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    """Test XML failure."""
    fs.add_real_file(xml_filepath)
    cfg = ConfigFile(name='tests')
    cfg.load(filepath=xml_filepath)

    with pytest.raises(CompendiumConfigFileError):
        cfg.create('/test', 'test')
        cfg.dump('./test.xml')
