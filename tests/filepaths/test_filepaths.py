import os

from compendium.config_manager import ConfigPaths


def test_singleton(fs):
    config_files = ConfigPaths(
        application='test'
    )

    # Singleton path
    fs.create_file('/opt/test/settings.toml')

    config_files.load_configs('/opt/test/settings.toml')
    filepaths = config_files.filepaths

    assert '/opt/test/settings.toml' in filepaths


def test_hierarchy(fs):
    user_path = os.path.expanduser('~')
    current_path = os.path.basename(__file__)
    config_files = ConfigPaths(
        application='test',
        load_strategy='hierarchy',
        enable_system_paths=True,
        enable_user_paths=True
    )

    # System path
    fs.create_file('/etc/test/settings.toml')

    # User path
    fs.create_file(user_path + '/.test.toml')
    fs.create_file(user_path + '/.test.d/settings.toml')

    # Current path
    fs.create_file(current_path + '/settings.toml')
    fs.create_file(current_path + '/test.toml')

    config_files.load_configs()
    filepaths = config_files.filepaths

    assert '/etc/test/settings.toml' in filepaths
    assert (user_path + '/.test.toml') in filepaths
    assert (user_path + '/.test.d/settings.toml') in filepaths


def test_nested(fs):
    current_path = os.path.basename(__file__) + '/nested'
    config_files = ConfigPaths(application='test', load_strategy='nested')

    # Current path
    fs.create_file(current_path + '/settings.toml')
    fs.create_file(current_path + '/example1/settings.toml')
    fs.create_file(current_path + '/example2/settings.toml')

    config_files.load_configs()
    filepaths = config_files.filepaths

    assert (current_path + '/settings.toml') in filepaths
    assert (current_path + '/example1/settings.toml') in filepaths
    assert (current_path + '/example2/settings.toml') in filepaths
