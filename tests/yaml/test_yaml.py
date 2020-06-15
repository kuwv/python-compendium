import os

from compendium.config_manager import ConfigPaths
from compendium.settings import Settings

config_path = os.path.dirname(os.path.realpath(__file__))
yaml_path = config_path + '/test.yaml'


def test_empty_filepath():
    empty_list = ConfigPaths(application='empty', filename='test.yaml')
    empty_list.load_configs()
    assert not empty_list.filepaths


def test_yaml_path(fs):
    fs.add_real_file(yaml_path)
    yaml_config = ConfigPaths(application='yaml', filename='test.yaml')
    yaml_config.load_config_filepath(config_path + '/test.yaml')
    assert "{}/test.yaml".format(config_path) in yaml_config.filepaths


def test_yaml_content(fs):
    fs.add_real_file(yaml_path)
    content = Settings(application='tests', path=yaml_path)
    content.load()
    assert content.get('.stooges.stooge1') == 'Larry'
    assert content.get('.stooges.stooge2') == 'Curly'
    assert content.get('.stooges.stooge3') == 'Moe'
    assert content.get('.fruit') != 'banana'
    assert content.get('.number') == 2


def test_yaml_content_save(fs):
    fs.add_real_file(yaml_path, False)
    settings = Settings(application='tests', path=yaml_path)
    settings.load()
    settings.create('.test', 'test')
    assert settings.settings['test'] == 'test'
