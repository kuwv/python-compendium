# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
# type: ignore
"""Test settings management."""

import os

from compendium.config_manager import ConfigManager

config_filepath = os.path.dirname(os.path.realpath(__file__))
settings_filepath = os.path.join(config_filepath, 'config.toml')


def test_filepath():
    """Test filepath loader."""
    cfg = ConfigManager(name='filepath', filepaths=[settings_filepath])
    cfg.load_configs()
    assert cfg.settings['title'] == 'TOML Example'


def test_defaults():
    """Test default settings."""
    cfg = ConfigManager(name='defaults', defaults={'default': 'result'})
    assert cfg.defaults == {'default': 'result'}
    result = cfg.settings.lookup('/default')
    assert result == 'result'


def test_settings():
    """Test default settings."""
    cfg = ConfigManager({'test': 'result'})
    assert cfg.settings == {'test': 'result'}
    result = cfg.settings.lookup('/test')
    assert result == 'result'


def test_environment():
    """Test environment variables."""
    os.environ['TESTS_KEY'] = 'test'
    cfg = ConfigManager(name='environs', prefix='tests')
    assert cfg.environs['key'] == 'test'
    assert cfg.settings.lookup('/key') == 'test'
