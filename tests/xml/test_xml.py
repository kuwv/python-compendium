# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Test XML content management.'''

import os
import pytest  # type: ignore

from compendium.config.paths import ConfigPaths
from compendium.config_manager import ConfigManager

config_path = os.path.dirname(os.path.realpath(__file__))
xml_path = config_path + '/test.xml'


def test_empty_filepath():
    '''Test XML filepth.'''
    cfg = ConfigPaths(application='empty', filename='test.xml')
    cfg.load_configs()
    assert not cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_xml_path(fs):
    '''Test XML path.'''
    fs.add_real_file(xml_path)
    cfg = ConfigPaths(application='tests', filename='test.xml')
    cfg.load_config_filepath(config_path + '/test.xml')
    assert "{}/test.xml".format(config_path) in cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_xml_content(fs):
    '''Test XML content read.'''
    fs.add_real_file(xml_path)
    cfg = ConfigManager(application='tests', path=xml_path)
    cfg.load()
    assert cfg.get('/root/stooges/stooge1') == 'Larry'
    assert cfg.get('/root/stooges/stooge2') == 'Curly'
    assert cfg.get('/root/stooges/stooge3') == 'Moe'
    assert cfg.get('/root/fruit') != 'banana'
    assert cfg.get('/root/number') == '2'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_xml_content_save(fs):
    '''Test XML content save.'''
    fs.add_real_file(xml_path, False)
    cfg = ConfigManager(application='tests', path=xml_path, writable=True)
    cfg.load()
    cfg.create('/root/test', 'test')
    assert cfg.get('/root/test') == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    '''Test XML failure.'''
    fs.add_real_file(xml_path)
    cfg = ConfigManager(application='tests', path=xml_path)
    cfg.load()

    with pytest.raises(IOError):
        cfg.create('/test', 'test')
        cfg.save('./test.xml')
