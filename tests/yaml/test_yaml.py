# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Test YAML configuration management.'''

import os
import pytest  # type: ignore

from compendium.loader import ConfigFile
# from compendium.exceptions import CompendiumConfigFileError

config_filepath = os.path.dirname(os.path.realpath(__file__))
yaml_filepath = os.path.join(config_filepath, 'test.yaml')


# def test_empty_filepath():
#     '''Test empty file.'''
#     cfg = ConfigFile(name='empty')
#     cfg.load_configs(filepath=yaml_filepath)
#     assert not cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_yaml_filepath(fs):
    '''Test YAML paths.'''
    fs.add_real_file(yaml_filepath)
    cfg = ConfigFile(
        name='yaml',
        filepath=os.path.join(config_filepath, 'test.yaml')
    )
    assert "{}/test.yaml".format(config_filepath) == cfg.filepath


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_yaml_content(fs):
    '''Test read YAML content.'''
    fs.add_real_file(yaml_filepath)
    cfg = ConfigFile(name='tests')
    cfg.load(filepath=yaml_filepath)
    assert cfg.retrieve('/stooges/stooge1') == 'Larry'
    assert cfg.retrieve('/stooges/stooge2') == 'Curly'
    assert cfg.retrieve('/stooges/stooge3') == 'Moe'
    assert cfg.retrieve('/fruit') != 'banana'
    assert cfg.retrieve('/number') == 2


# @pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
# def test_yaml_content_dump(fs):
#     '''Test YAML content save.'''
#     fs.add_real_file(yaml_filepath, False)
#     cfg = ConfigFile(name='tests', writable=True)
#     cfg.load(filepath=yaml_filepath)
#     cfg.create('/test', 'test')
#     assert cfg['test'] == 'test'
#
#
# @pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
# def test_cfg_save_fail(fs):
#     '''Test YAML content fail.'''
#     fs.add_real_file(yaml_filepath)
#     cfg = ConfigFile(name='tests')
#     cfg.load(filepath=yaml_filepath)
#
#     with pytest.raises(CompendiumConfigFileError):
#         cfg.create('/test', 'test')
#         cfg.dump('./test.yaml')
