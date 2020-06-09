import os
from compendium.config_manager import ConfigManager


def test_hierarchy(fs):
    user_path = os.path.expanduser('~')
    current_path = os.path.basename(__file__)
    config_files = ConfigManager(
        application='test', enable_system_paths=True, enable_user_paths=True
    )

    # System path
    fs.create_file('/etc/test/settings.toml')

    # User path
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


# def test_nested(fs):
#     current_path = os.path.basename(__file__)
#     config_files = ConfigManager(application='test')
#
#     # Current path
#     fs.create_file(current_path + '/settings.toml')
#     fs.create_file(current_path + '/example1/settings.toml')
#     fs.create_file(current_path + '/example2/settings.toml')
#
#     config_files.load_config_paths()
#     filepaths = config_files.filepaths
#     print('Filepaths: ' + str(filepaths))
#
#     assert (current_path + '/settings.toml') in filepaths
#     assert (current_path + '/example1/settings.toml') in filepaths
#     assert (current_path + '/example2/settings.toml') in filepaths
