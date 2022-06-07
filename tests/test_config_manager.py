# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
# type: ignore
"""Test settings management."""

import os

from compendium.config_manager import ConfigManager

basedir = os.path.dirname(__file__)
filepath = os.path.join(basedir, 'config.toml')


def test_filepath():
    """Test filepath loader."""
    cfg = ConfigManager(name='filepath', filepaths=[filepath])
    cfg.load_configs()
    assert cfg['title'] == 'TOML Example'


def test_defaults():
    """Test default settings."""
    cfg = ConfigManager(name='defaults', defaults={'default': 'result'})
    assert cfg.defaults == {'default': 'result'}
    assert cfg.get('/default') == 'result'


def test_settings():
    """Test default settings."""
    cfg = ConfigManager({'test': 'result'})
    assert cfg.data == {'test': 'result'}
    assert cfg.get('/test') == 'result'


def test_environment():
    """Test environment variables."""
    os.environ['TESTS_KEY'] = 'test'
    assert os.getenv('TESTS_KEY') == 'test'

    cfg = ConfigManager(name='environs', prefix='TESTS')
    assert cfg['/key'] == 'test'
    assert cfg.environs == {'key': 'test'}
    assert cfg.get('/key') == 'test'
    assert cfg.get('/nothing', 'nada') == 'nada'
    assert cfg.lookup('/key') == 'test'
    assert cfg.lookup('/nothing', '/key', default='nada') == 'test'
