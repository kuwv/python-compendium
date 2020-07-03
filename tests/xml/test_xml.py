import os
import pytest

from compendium.config.paths import ConfigPaths
from compendium.settings import Settings

config_path = os.path.dirname(os.path.realpath(__file__))
xml_path = config_path + '/test.xml'


def test_empty_filepath():
    cfg = ConfigPaths(application='empty', filename='test.xml')
    cfg.load_configs()
    assert not cfg.filepaths


def test_xml_path(fs):
    fs.add_real_file(xml_path)
    cfg = ConfigPaths(application='tests', filename='test.xml')
    cfg.load_config_filepath(config_path + '/test.xml')
    assert "{}/test.xml".format(config_path) in cfg.filepaths


def test_xml_content(fs):
    fs.add_real_file(xml_path)
    cfg = Settings(application='tests', path=xml_path)
    cfg.load()
    assert cfg.get('/root/stooges/stooge1') == 'Larry'
    assert cfg.get('/root/stooges/stooge2') == 'Curly'
    assert cfg.get('/root/stooges/stooge3') == 'Moe'
    assert cfg.get('/root/fruit') != 'banana'
    assert cfg.get('/root/number') == '2'


def test_xml_content_save(fs):
    fs.add_real_file(xml_path, False)
    cfg = Settings(application='tests', path=xml_path, writable=True)
    cfg.load()
    cfg.create('/root/test', 'test')
    assert cfg.get('/root/test') == 'test'


def test_cfg_save_fail(fs):
    fs.add_real_file(xml_path)
    cfg = Settings(application='tests', path=xml_path)
    cfg.load()

    with pytest.raises(IOError):
        cfg.create('/test', 'test')
