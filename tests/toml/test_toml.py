import os

from compendium.config_manager import ConfigPaths
from compendium.settings import Settings

config_path = os.path.dirname(os.path.realpath(__file__))
toml_path = config_path + '/test.toml'


def test_empty_filepath():
    empty_list = ConfigPaths(application='empty', filename='test.toml')
    empty_list.load_configs()
    assert not empty_list.filepaths


def test_toml_path(fs):
    fs.add_real_file(toml_path)
    toml_config = ConfigPaths(application='toml', filename='test.toml')
    toml_config.load_config_filepath(config_path + '/test.toml')
    assert "{}/test.toml".format(config_path) in toml_config.filepaths


def test_toml_content(fs):
    fs.add_real_file(toml_path)
    content = Settings(application='tests', path=toml_path)
    content.load()
    assert content.get('.stooges.stooge1') == 'Larry'
    assert content.get('.stooges.stooge2') == 'Curly'
    assert content.get('.stooges.stooge3') == 'Moe'
    assert content.get('.fruit') != 'banana'
    assert content.get('.number') == 2


def test_toml_content_save(fs):
    fs.add_real_file(toml_path, False)
    settings = Settings(application='tests', path=toml_path)
    settings.load()
    settings.create('.test', 'test')
    assert settings.settings['test'] == 'test'
