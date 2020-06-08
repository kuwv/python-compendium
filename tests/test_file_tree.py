from compendium.config_manager import ConfigManager
import os


def test_config_manager(fs):
    user_path = os.path.expanduser('~')
    current_path = os.path.basename(__file__)
    config_files = ConfigManager(application='test')

    # System path
    fs.create_file('/etc/test/settings.toml')

    # Home path
    fs.create_file(user_path + '/.test.toml')
    fs.create_file(user_path + '/.test.d/settings.toml')

    # Current path
    fs.create_file(current_path + '/settings.toml')
    fs.create_file(current_path + '/test.toml')

    config_files.load_config_paths()
    filepaths = config_files.filepaths
    print('Filepaths: ' + str(filepaths))

    assert '/etc/test/settings.toml' in filepaths
    assert (user_path + '/.test.toml') in filepaths
    assert (user_path + '/.test.d/settings.toml') in filepaths
    # TODO: missing current_path
