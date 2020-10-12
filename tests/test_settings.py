# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
'''Test settings management.'''

import os

import pytest  # type: ignore

from compendium.config_manager import ConfigManager

config_path = os.path.dirname(os.path.realpath(__file__))
settings_path = os.path.join(config_path, 'settings.toml')


# @pytest.fixture(params=['fs', [[['pkgutil']]]])
# def cfg(fs):
#     fs.add_real_file(settings_path, False)
#     cfg = ConfigManager(application='tests', path=settings_path)
#     cfg.load()
#     return cfg
#
# def test_result(cfg):
#     result = cfg.search('/servers/**/ip')
#     assert ['10.0.0.1', '10.0.0.2'] == result


def test_default():
    '''Test default settings.'''
    cfg = ConfigManager(application='tests', defaults={'default': 'result'})
    defaults = cfg.defaults
    assert defaults == {'default': 'result'}
    result = cfg.get('default')
    assert result == 'result'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_result(fs):
    '''Test IP from settings.'''
    fs.add_real_file(settings_path, False)
    cfg = ConfigManager(application='tests')
    cfg.load(settings_path)
    result = cfg.search('/servers/**/ip')
    assert ['10.0.0.1', '10.0.0.2'] == result


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content_create(fs):
    '''Test content creation settings.'''
    fs.add_real_file(settings_path, False)
    cfg = ConfigManager(application='tests', path=settings_path)
    cfg.load()
    cfg.create('/test', 'test')
    assert cfg.get('test') == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content_append(fs):
    '''Test appending settings to list.'''
    fs.add_real_file(settings_path, False)
    cfg = ConfigManager(application='tests', path=settings_path)
    cfg.load()
    cfg.append('/database/ports', 2345)
    assert 2345 in cfg.get('/database/ports')


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content_update(fs):
    '''Test content update.'''
    fs.add_real_file(settings_path, False)
    cfg = ConfigManager(application='tests', path=settings_path, writable=True)
    cfg.load()
    cfg.update('/owner/name', 'Tom Waits')
    assert cfg.get('/owner/name') == 'Tom Waits'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_delete(fs):
    '''Test content deletion.'''
    fs.add_real_file(settings_path, False)
    cfg = ConfigManager(application='tests', path=settings_path)
    cfg.load()
    assert cfg.search('/owner/name') == ['Tom Preston-Werner']
    cfg.delete('/owner/name')
    assert cfg.search('/owner/name') == []
