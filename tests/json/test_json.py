from compendium.config_manager import ConfigManager
from compendium.settings import Settings
from jmespath import search
import os

settings_path = os.path.dirname(os.path.realpath(__file__))
json_path = settings_path + '/test.json'


def test_empty_filepath(fs):
    empty_content = ConfigManager(application='empty', filename='test.json')
    empty_content.load()
    assert not empty_content.filepaths


def test_json_path(fs):
    fs.add_real_file(json_path)
    json_content = ConfigManager(application='json', filename='test.json')
    json_content.load_config(settings_path + '/test.json')
    assert "{}/test.json".format(settings_path) in json_content.filepaths


def test_json_content(fs):
    fs.add_real_file(json_path)
    settings = Settings(application='tests', path=json_path)
    print(settings.settings)
    assert search('stooges.stooge1', settings.settings) == 'Larry'
    assert search('stooges.stooge2', settings.settings) == 'Curly'
    assert search('stooges.stooge3', settings.settings) == 'Moe'
    assert search('fruit', settings.settings) != 'banana'
    assert search('number', settings.settings) == 2


def test_json_content_save(fs):
    fs.add_real_file(json_path)
    settings = Settings(application='tests', path=json_path)
    settings.update({'test': 'test'})
