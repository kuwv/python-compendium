from compendium.config_manager import ConfigManager
from compendium.settings import Settings
from jmespath import search
import os

config_path = os.path.dirname(os.path.realpath(__file__))
json_path = config_path + '/test.json'


def test_empty_filepath():
    empty_list = ConfigManager(application='empty', filename='test.json')
    empty_list.load_config_paths()
    assert not empty_list.filepaths


def test_json_path(fs):
    fs.add_real_file(json_path)
    json_config = ConfigManager(application='json', filename='test.json')
    json_config.load_config_path(config_path + '/test.json')
    assert "{}/test.json".format(config_path) in json_config.filepaths


def test_json_content(fs):
    fs.add_real_file(json_path)
    config = Settings(application='tests', path=json_path)
    assert search('stooges.stooge1', config.settings) == 'Larry'
    assert search('stooges.stooge2', config.settings) == 'Curly'
    assert search('stooges.stooge3', config.settings) == 'Moe'
    assert search('fruit', config.settings) != 'banana'
    assert search('number', config.settings) == 2

def test_json_content():
    config = Settings(application='tests', path=json_path)
    config.update_settings({'test': 'test'})
    config.save_settings()
