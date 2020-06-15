import os

from compendium.config_manager import ConfigPaths
from compendium.settings import Settings

settings_path = os.path.dirname(os.path.realpath(__file__))
json_path = settings_path + '/test.json'


def test_empty_filepath(fs):
    empty_content = ConfigPaths(application='empty', filename='test.json')
    empty_content.load_configs()
    assert not empty_content.filepaths


def test_json_path(fs):
    fs.add_real_file(json_path)
    json_content = ConfigPaths(application='json', filename='test.json')
    json_content.load_config_filepath(settings_path + '/test.json')
    assert "{}/test.json".format(settings_path) in json_content.filepaths


def test_json_content(fs):
    fs.add_real_file(json_path)
    content = Settings(application='tests', path=json_path)
    content.load()
    assert content.get('.stooges.stooge1') == 'Larry'
    assert content.get('.stooges.stooge2') == 'Curly'
    assert content.get('.stooges.stooge3') == 'Moe'
    assert content.get('.fruit') != 'banana'
    assert content.get('.number') == 2


def test_json_content_save(fs):
    fs.add_real_file(json_path, False)
    settings = Settings(application='tests', path=json_path)
    settings.load()
    settings.create('.test', 'test')
    assert settings.settings['test'] == 'test'
