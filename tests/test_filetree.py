from compendium import filetree  # , settings
import os


def test_filetree(fs):
    user_path = os.path.expanduser('~')
    current_path = os.path.basename(__file__)
    filetree_list = filetree.FileTree(application='test')

    # System path
    fs.create_file('/etc/test/settings.toml')

    # Home path
    fs.create_file(user_path + '/.test.toml')
    fs.create_file(user_path + '/.test.d/settings.toml')

    # Current path
    fs.create_file(current_path + '/settings.toml')
    fs.create_file(current_path + '/test.toml')

    filetree_list.load_config_paths()
    filepaths = filetree_list.filepaths
    print('Filepaths: ' + str(filepaths))

    assert '/etc/test/settings.toml' in filepaths
    assert (user_path + '/.test.toml') in filepaths
    assert (user_path + '/.test.d/settings.toml') in filepaths
    # TODO: missing current_path
