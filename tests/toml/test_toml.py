# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Test TOML configuration management.'''

import os
import pytest  # type: ignore

from compendium.config_manager import ConfigManager

config_filepath = os.path.dirname(os.path.realpath(__file__))
toml_filepath = os.path.join(config_filepath, 'test.toml')


# def test_empty_filepath():
#     '''Test empty file.'''
#     cfg = ConfigManager(application='empty', filename='test.toml')
#     cfg.load()
#     assert not cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_filepath(fs):
    '''Test TOML filepaths.'''
    fs.add_real_file(toml_filepath)
    cfg = ConfigManager(application='toml', filename='test.toml')
    cfg.load_filepath(os.path.join(config_filepath, 'test.toml'))
    assert "{}/test.toml".format(config_filepath) in cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content(fs):
    '''Test TOML content load.'''
    fs.add_real_file(toml_filepath)
    cfg = ConfigManager(application='tests')
    cfg.load(filepath=toml_filepath)
    assert cfg.settings.get('/stooges/stooge1') == 'Larry'
    assert cfg.settings.get('/stooges/stooge2') == 'Curly'
    assert cfg.settings.get('/stooges/stooge3') == 'Moe'
    assert cfg.settings.get('/fruit') != 'banana'
    assert cfg.settings.get('/number') == 2


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content_dump(fs):
    '''Test TOML content save.'''
    fs.add_real_file(toml_filepath, False)
    cfg = ConfigManager(application='tests', writable=True)
    cfg.load(filepath=toml_filepath)
    cfg.settings.create('/test', 'test')
    assert cfg.settings.get('test') == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    '''Test TOML content failure.'''
    fs.add_real_file(toml_filepath)
    cfg = ConfigManager(application='tests')
    cfg.load(filepath=toml_filepath)

    with pytest.raises(IOError):
        cfg.settings.create('/test', 'test')
        cfg.dump('./test.toml')
