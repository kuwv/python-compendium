# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Test YAML configuration management.'''

import os
import pytest  # type: ignore

from compendium.config_manager import ConfigManager
# from compendium.exceptions import CompendiumConfigFileError

config_filepath = os.path.dirname(os.path.realpath(__file__))
yaml_filepath = os.path.join(config_filepath, 'test.yaml')


# def test_empty_filepath():
#     '''Test empty file.'''
#     cfg = ConfigManager(application='empty')
#     cfg.load_configs(filepath=yaml_filepath)
#     assert not cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_yaml_filepath(fs):
    '''Test YAML paths.'''
    fs.add_real_file(yaml_filepath)
    cfg = ConfigManager(application='yaml')
    cfg.load_filepath(os.path.join(config_filepath, 'test.yaml'))
    assert "{}/test.yaml".format(config_filepath) in cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_yaml_content(fs):
    '''Test read YAML content.'''
    fs.add_real_file(yaml_filepath)
    cfg = ConfigManager(application='tests')
    cfg.load(filepath=yaml_filepath)
    assert cfg.settings.get('/stooges/stooge1') == 'Larry'
    assert cfg.settings.get('/stooges/stooge2') == 'Curly'
    assert cfg.settings.get('/stooges/stooge3') == 'Moe'
    assert cfg.settings.get('/fruit') != 'banana'
    assert cfg.settings.get('/number') == 2


# @pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
# def test_yaml_content_dump(fs):
#     '''Test YAML content save.'''
#     fs.add_real_file(yaml_filepath, False)
#     cfg = ConfigManager(application='tests', writable=True)
#     cfg.load(filepath=yaml_filepath)
#     cfg.create('/test', 'test')
#     assert cfg.settings['test'] == 'test'
#
#
# @pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
# def test_cfg_save_fail(fs):
#     '''Test YAML content fail.'''
#     fs.add_real_file(yaml_filepath)
#     cfg = ConfigManager(application='tests')
#     cfg.load(filepath=yaml_filepath)
#
#     with pytest.raises(CompendiumConfigFileError):
#         cfg.create('/test', 'test')
#         cfg.dump('./test.yaml')
