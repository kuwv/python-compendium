# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Test JSON content management.'''

import os
import pytest  # type: ignore

from compendium.config_manager import ConfigManager

settings_filepath = os.path.dirname(os.path.realpath(__file__))
json_filepath = os.path.join(settings_filepath, 'test.json')


# @pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
# def test_empty_filepath(fs):
#     '''Test empty file.'''
#     cfg = ConfigPaths(application='empty')
#     cfg.load_configs(filename='test.json')
#     assert not cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_json_filepath(fs):
    '''Test JSON filepaths.'''
    fs.add_real_file(json_filepath)
    cfg = ConfigManager(application='json', filename='test.json')
    cfg.load_filepath(os.path.join(settings_filepath, 'test.json'))
    assert "{}/test.json".format(settings_filepath) in cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg(fs):
    '''Test loading JSON configuration.'''
    fs.add_real_file(json_filepath)
    cfg = ConfigManager(application='tests')
    cfg.load(filepath=json_filepath)
    assert cfg.get('/stooges/stooge1') == 'Larry'
    assert cfg.get('/stooges/stooge2') == 'Curly'
    assert cfg.get('/stooges/stooge3') == 'Moe'
    assert cfg.get('/fruit') != 'banana'
    assert cfg.get('/number') == 2


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_dump(fs):
    '''Test saving JSON content.'''
    fs.add_real_file(json_filepath, False)
    cfg = ConfigManager(application='tests', writable=True)
    cfg.load(filepath=json_filepath)
    cfg.create('/test', 'test')
    assert cfg.settings['test'] == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    '''Test JSON failure.'''
    fs.add_real_file(json_filepath)
    cfg = ConfigManager(application='tests')
    cfg.load(filepath=json_filepath)

    with pytest.raises(IOError):
        cfg.create('/test', 'test')
        cfg.dump('./test.json')
