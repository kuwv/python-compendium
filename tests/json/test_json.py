from compendium.config_manager import ConfigManager
from compendium.settings import Settings
from jmespath import search
import os

settings_path = os.path.dirname(os.path.realpath(__file__))
json_path = settings_path + '/test.json'


def test_empty_filepath():
    empty_list = ConfigManager(application='empty', filename='test.json')
    empty_list.load()
    assert not empty_list.filepaths


def test_json_path(fs):
    fs.add_real_file(json_path)
    json_settings = ConfigManager(application='json', filename='test.json')
    json_settings.load_config_path(settings_path + '/test.json')
    assert "{}/test.json".format(settings_path) in json_settings.filepaths


def test_json_content(fs):
    fs.add_real_file(json_path)
    settings = Settings(application='tests', path=json_path)
    assert search('stooges.stooge1', settings.settings) == 'Larry'
    assert search('stooges.stooge2', settings.settings) == 'Curly'
    assert search('stooges.stooge3', settings.settings) == 'Moe'
    assert search('fruit', settings.settings) != 'banana'
    assert search('number', settings.settings) == 2


def test_json_content_save():
    settings = Settings(application='tests', path=json_path)
    settings.update({'test': 'test'})
