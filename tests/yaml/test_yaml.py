import os
import pytest

from compendium.config.paths import ConfigPaths
from compendium.settings import Settings

config_path = os.path.dirname(os.path.realpath(__file__))
yaml_path = config_path + '/test.yaml'


def test_empty_filepath():
    cfg = ConfigPaths(application='empty', filename='test.yaml')
    cfg.load_configs()
    assert not cfg.filepaths


def test_yaml_path(fs):
    fs.add_real_file(yaml_path)
    cfg = ConfigPaths(application='yaml', filename='test.yaml')
    cfg.load_config_filepath(config_path + '/test.yaml')
    assert "{}/test.yaml".format(config_path) in cfg.filepaths


def test_yaml_content(fs):
    fs.add_real_file(yaml_path)
    cfg = Settings(application='tests', path=yaml_path)
    cfg.load()
    assert cfg.get('/stooges/stooge1') == 'Larry'
    assert cfg.get('/stooges/stooge2') == 'Curly'
    assert cfg.get('/stooges/stooge3') == 'Moe'
    assert cfg.get('/fruit') != 'banana'
    assert cfg.get('/number') == 2


def test_yaml_content_save(fs):
    fs.add_real_file(yaml_path, False)
    cfg = Settings(application='tests', path=yaml_path, writable=True)
    cfg.load()
    cfg.create('/test', 'test')
    assert cfg.settings['test'] == 'test'


def test_cfg_save_fail(fs):
    fs.add_real_file(yaml_path)
    cfg = Settings(application='tests', path=yaml_path)
    cfg.load()

    with pytest.raises(IOError):
        cfg.create('/test', 'test')
