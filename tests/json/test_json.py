import os

from jmespath import search

from compendium.config_manager import ConfigLayout
from compendium.settings import Settings

settings_path = os.path.dirname(os.path.realpath(__file__))
json_path = settings_path + '/test.json'


def test_empty_filepath(fs):
    empty_content = ConfigLayout(application='empty', filename='test.json')
    empty_content.load_configs()
    assert not empty_content.filepaths


def test_json_path(fs):
    fs.add_real_file(json_path)
    json_content = ConfigLayout(application='json', filename='test.json')
    json_content.load_config(settings_path + '/test.json')
    assert "{}/test.json".format(settings_path) in json_content.filepaths


def test_json_content(fs):
    fs.add_real_file(json_path)
    settings = Settings(application='tests', path=json_path)
    assert search('stooges.stooge1', settings.settings) == 'Larry'
    assert search('stooges.stooge2', settings.settings) == 'Curly'
    assert search('stooges.stooge3', settings.settings) == 'Moe'
    assert search('fruit', settings.settings) != 'banana'
    assert search('number', settings.settings) == 2


def test_json_content_save(fs):
    fs.add_real_file(json_path, False)
    settings = Settings(application='tests', path=json_path)
    settings.update({'test': 'test'})
    assert settings.settings['test'] == 'test'
