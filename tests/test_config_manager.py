# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
'''Test settings management.'''

import os

from compendium.config_manager import ConfigManager

config_filepath = os.path.dirname(os.path.realpath(__file__))
settings_filepath = os.path.join(config_filepath, 'config.toml')


def test_filepath():
    '''Test filepath loader.'''
    cfg = ConfigManager(settings_filepath, name='filepath')
    cfg.load_configs()
    assert cfg.settings['title'] == 'TOML Example'


def test_defaults():
    '''Test default settings.'''
    cfg = ConfigManager(name='defaults', defaults={'default': 'result'})
    assert cfg.defaults == {'default': 'result'}
    result = cfg.settings.retrieve('/default')
    assert result == 'result'


def test_environment():
    '''Test environment variables.'''
    os.environ['TESTS_KEY'] = 'test'
    cfg = ConfigManager(name='environs', prefix='tests')
    assert cfg.environs['key'] == 'test'
    assert cfg.settings.retrieve('/key') == 'test'
