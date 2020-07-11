import os
from os.path import join

from compendium.config.paths import ConfigPaths


def test_singleton(fs):
    # Setup Singleton path
    fs.create_file('/opt/test/settings.toml')

    # Test Singleton
    cfg = ConfigPaths(application='test')
    cfg.load_configs('/opt/test/settings.toml')

    assert '/opt/test/settings.toml' in cfg.filepaths


def test_hierarchy(fs):
    # Setup base paths
    user_path = os.path.expanduser('~')
    base_filepath = os.path.basename(__file__)

    # System path
    fs.create_file('/etc/test/settings.toml')

    # User path
    fs.create_file(join(user_path, '.test.toml'))
    fs.create_file(join(user_path, '.test.d', 'settings.toml'))

    # Current path
    fs.create_file(join(base_filepath, 'settings.toml'))
    fs.create_file(join(base_filepath, 'test.toml'))

    # Test hierarchy
    cfg = ConfigPaths(
        application='test',
        load_strategy='hierarchy',
        enable_system_paths=True,
        enable_user_paths=True
    )
    cfg.load_configs()

    assert '/etc/test/settings.toml' in cfg.filepaths
    assert (join(user_path, '.test.toml')) in cfg.filepaths
    assert (join(user_path, '.test.d', 'settings.toml')) in cfg.filepaths


def test_nested(fs):
    # Setup base paths
    base_filepath = os.path.dirname(os.path.realpath(__file__))

    # Current path
    fs.create_file(join(base_filepath, 'settings.toml'))
    fs.create_file(join(base_filepath, 'example1', 'settings.toml'))
    fs.create_file(join(base_filepath, 'example2', 'settings.toml'))

    # Test nested
    cfg = ConfigPaths(application='test', load_strategy='nested')
    cfg.load_configs()

    assert (join(base_filepath, 'settings.toml')) in cfg.filepaths
    assert (join(base_filepath, 'example1', 'settings.toml')) in cfg.filepaths
    assert (join(base_filepath, 'example2', 'settings.toml')) in cfg.filepaths
