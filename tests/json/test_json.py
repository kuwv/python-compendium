# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Test JSON content management.'''

import os
import pytest  # type: ignore

from compendium.config.paths import ConfigPaths
from compendium.config_manager import ConfigManager

settings_path = os.path.dirname(os.path.realpath(__file__))
json_path = settings_path + '/test.json'


# @pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
# def test_empty_filepath(fs):
#     '''Test empty file.'''
#     cfg = ConfigPaths(application='empty', filename='test.json')
#     cfg.load_configs()
#     assert not cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_json_path(fs):
    '''Test JSON filepaths.'''
    fs.add_real_file(json_path)
    cfg = ConfigPaths(application='json', filename='test.json')
    cfg.load_filepath(settings_path + '/test.json')
    assert "{}/test.json".format(settings_path) in cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg(fs):
    '''Test loading JSON configuration.'''
    fs.add_real_file(json_path)
    cfg = ConfigManager(application='tests', path=json_path)
    cfg.load()
    assert cfg.get('/stooges/stooge1') == 'Larry'
    assert cfg.get('/stooges/stooge2') == 'Curly'
    assert cfg.get('/stooges/stooge3') == 'Moe'
    assert cfg.get('/fruit') != 'banana'
    assert cfg.get('/number') == 2


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save(fs):
    '''Test saving JSON content.'''
    fs.add_real_file(json_path, False)
    cfg = ConfigManager(application='tests', path=json_path, writable=True)
    cfg.load()
    cfg.create('/test', 'test')
    assert cfg.settings['test'] == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    '''Test JSON failure.'''
    fs.add_real_file(json_path)
    cfg = ConfigManager(application='tests', path=json_path)
    cfg.load()

    with pytest.raises(IOError):
        cfg.create('/test', 'test')
        cfg.save('./test.json')
