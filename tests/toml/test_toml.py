# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Test TOML configuration management.'''

import os
import pytest  # type: ignore

from compendium.config.paths import ConfigPaths
from compendium.config_manager import ConfigManager

config_path = os.path.dirname(os.path.realpath(__file__))
toml_path = config_path + '/test.toml'


def test_empty_filepath():
    '''Test empty file.'''
    cfg = ConfigPaths(application='empty', filename='test.toml')
    cfg.load_configs()
    assert not cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_path(fs):
    '''Test TOML filepaths.'''
    fs.add_real_file(toml_path)
    cfg = ConfigPaths(application='toml', filename='test.toml')
    cfg.load_config_filepath(config_path + '/test.toml')
    assert "{}/test.toml".format(config_path) in cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content(fs):
    '''Test TOML content load.'''
    fs.add_real_file(toml_path)
    cfg = ConfigManager(application='tests', path=toml_path)
    cfg.load()
    assert cfg.get('/stooges/stooge1') == 'Larry'
    assert cfg.get('/stooges/stooge2') == 'Curly'
    assert cfg.get('/stooges/stooge3') == 'Moe'
    assert cfg.get('/fruit') != 'banana'
    assert cfg.get('/number') == 2


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content_save(fs):
    '''Test TOML content save.'''
    fs.add_real_file(toml_path, False)
    cfg = ConfigManager(application='tests', path=toml_path, writable=True)
    cfg.load()
    cfg.create('/test', 'test')
    assert cfg.settings['test'] == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    '''Test TOML content failure.'''
    fs.add_real_file(toml_path)
    cfg = ConfigManager(application='tests', path=toml_path)
    cfg.load()

    with pytest.raises(IOError):
        cfg.create('/test', 'test')
        cfg.save('./test.toml')
