# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Test XML content management.'''

import os
import pytest  # type: ignore

from compendium.config_manager import ConfigManager

config_filepath = os.path.dirname(os.path.realpath(__file__))
xml_filepath = os.path.join(config_filepath, 'test.xml')


# def test_empty_filepath():
#     '''Test XML filepth.'''
#     cfg = ConfigPaths(application='empty')
#     cfg.load_configs(filename='test.xml')
#     assert not cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_xml_filepath(fs):
    '''Test XML path.'''
    fs.add_real_file(xml_filepath)
    cfg = ConfigManager(application='tests')
    cfg.load_filepath(os.path.join(config_filepath, 'test.xml'))
    assert "{}/test.xml".format(config_filepath) in cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_xml_content(fs):
    '''Test XML content read.'''
    fs.add_real_file(xml_filepath)
    cfg = ConfigManager(application='tests')
    cfg.load(filepath=xml_filepath)
    assert cfg.get('/root/stooges/stooge1') == 'Larry'
    assert cfg.get('/root/stooges/stooge2') == 'Curly'
    assert cfg.get('/root/stooges/stooge3') == 'Moe'
    assert cfg.get('/root/fruit') != 'banana'
    assert cfg.get('/root/number') == '2'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_xml_content_dump(fs):
    '''Test XML content save.'''
    fs.add_real_file(xml_filepath, False)
    cfg = ConfigManager(application='tests', writable=True)
    cfg.load(filepath=xml_filepath)
    cfg.create('/root/test', 'test')
    assert cfg.get('/root/test') == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    '''Test XML failure.'''
    fs.add_real_file(xml_filepath)
    cfg = ConfigManager(application='tests')
    cfg.load(filepath=xml_filepath)

    with pytest.raises(IOError):
        cfg.create('/test', 'test')
        cfg.dump('./test.xml')
