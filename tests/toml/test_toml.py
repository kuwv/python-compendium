from compendium.config_manager import ConfigManager
from compendium.settings import Settings
from jmespath import search
import os

config_path = os.path.dirname(os.path.realpath(__file__))
toml_path = config_path + '/test.toml'


def test_empty_filepath():
    empty_list = ConfigManager(application='empty', filename='test.toml')
    empty_list.load_config_paths()
    assert not empty_list.filepaths


def test_toml_path(fs):
    fs.add_real_file(toml_path)
    toml_config = ConfigManager(application='toml', filename='test.toml')
    toml_config.load_config_path(config_path + '/test.toml')
    assert "{}/test.toml".format(config_path) in toml_config.filepaths


def test_toml_content(fs):
    fs.add_real_file(toml_path)
    config = Settings(application='tests', path=toml_path)
    assert search('stooges.stooge1', config.settings) == 'Larry'
    assert search('stooges.stooge2', config.settings) == 'Curly'
    assert search('stooges.stooge3', config.settings) == 'Moe'
    assert search('fruit', config.settings) != 'banana'
    assert search('number', config.settings) == 2
