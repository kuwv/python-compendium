# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Test YAML configuration management.'''

import os
import pytest  # type: ignore

from compendium.config.paths import ConfigPaths
from compendium.config_manager import ConfigManager

config_path = os.path.dirname(os.path.realpath(__file__))
yaml_path = config_path + '/test.yaml'


# def test_empty_filepath():
#     '''Test empty file.'''
#     cfg = ConfigPaths(application='empty', filename='test.yaml')
#     cfg.load_configs()
#     assert not cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_yaml_path(fs):
    '''Test YAML paths.'''
    fs.add_real_file(yaml_path)
    cfg = ConfigPaths(application='yaml', filename='test.yaml')
    cfg.load_filepath(config_path + '/test.yaml')
    assert "{}/test.yaml".format(config_path) in cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_yaml_content(fs):
    '''Test read YAML content.'''
    fs.add_real_file(yaml_path)
    cfg = ConfigManager(application='tests', path=yaml_path)
    cfg.load()
    assert cfg.get('/stooges/stooge1') == 'Larry'
    assert cfg.get('/stooges/stooge2') == 'Curly'
    assert cfg.get('/stooges/stooge3') == 'Moe'
    assert cfg.get('/fruit') != 'banana'
    assert cfg.get('/number') == 2


# @pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
# def test_yaml_content_save(fs):
#     '''Test YAML content save.'''
#     fs.add_real_file(yaml_path, False)
#     cfg = ConfigManager(
#         application='tests', path=yaml_path, writable=True
#     )
#     cfg.load()
#     cfg.create('/test', 'test')
#     assert cfg.settings['test'] == 'test'


# @pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
# def test_cfg_save_fail(fs):
#     '''Test YAML content fail.'''
#     fs.add_real_file(yaml_path)
#     cfg = ConfigManager(application='tests', path=yaml_path)
#     cfg.load()
#
#     with pytest.raises(IOError):
#         cfg.create('/test', 'test')
#         cfg.save('./test.yaml')
