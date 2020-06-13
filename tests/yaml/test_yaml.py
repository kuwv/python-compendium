import os

from jmespath import search

from compendium.config_manager import ConfigLayout
from compendium.settings import Settings

config_path = os.path.dirname(os.path.realpath(__file__))
yaml_path = config_path + '/test.yaml'


def test_empty_filepath():
    empty_list = ConfigLayout(application='empty', filename='test.yaml')
    empty_list.load_configs()
    assert not empty_list.filepaths


def test_yaml_path(fs):
    fs.add_real_file(yaml_path)
    yaml_config = ConfigLayout(application='yaml', filename='test.yaml')
    yaml_config.load_config(config_path + '/test.yaml')
    assert "{}/test.yaml".format(config_path) in yaml_config.filepaths


def test_yaml_content(fs):
    fs.add_real_file(yaml_path)
    config = Settings(application='tests', path=yaml_path)
    assert search('stooges.stooge1', config.settings) == 'Larry'
    assert search('stooges.stooge2', config.settings) == 'Curly'
    assert search('stooges.stooge3', config.settings) == 'Moe'
    assert search('fruit', config.settings) != 'banana'
    assert search('number', config.settings) == 2


def test_yaml_content_save(fs):
    fs.add_real_file(yaml_path, False)
    settings = Settings(application='tests', path=yaml_path)
    settings.update({'test': 'test'})
    assert settings.settings['test'] == 'test'
