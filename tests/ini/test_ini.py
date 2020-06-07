from compendium.filetree import FileTree
from compendium.settings import Settings
from jmespath import search
import os

config_path = os.path.dirname(os.path.realpath(__file__))
ini_path = config_path + '/test.ini'


def test_empty_filepath():
    empty_list = FileTree(application='empty', filename='test.ini')
    empty_list.load_config_paths()
    assert not empty_list.filepaths


def test_ini_path(fs):
    fs.add_real_file(ini_path)
    ini_config = FileTree(application='ini', filename='test.ini')
    ini_config.load_config_path(config_path + '/test.ini')
    assert "{}/test.ini".format(config_path) in ini_config.filepaths


def test_ini_content(fs):
    fs.add_real_file(ini_path)
    config = Settings(application='tests', path=ini_path)
    assert search('stooges.stooge1', config.settings) == 'Larry'
    assert search('stooges.stooge2', config.settings) == 'Curly'
    assert search('stooges.stooge3', config.settings) == 'Moe'
    assert search('fruits.fruit', config.settings) != 'banana'
    assert search('numbers.number', config.settings) == '2'
