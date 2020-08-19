import os
import pytest

from compendium.config.paths import ConfigPaths
from compendium.settings import SingletonSettings

config_path = os.path.dirname(os.path.realpath(__file__))
toml_path = config_path + '/test.toml'


def test_empty_filepath():
    cfg = ConfigPaths(application='empty', filename='test.toml')
    cfg.load_configs()
    assert not cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_path(fs):
    fs.add_real_file(toml_path)
    cfg = ConfigPaths(application='toml', filename='test.toml')
    cfg.load_config_filepath(config_path + '/test.toml')
    assert "{}/test.toml".format(config_path) in cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content(fs):
    fs.add_real_file(toml_path)
    cfg = SingletonSettings(application='tests', path=toml_path)
    cfg.load()
    assert cfg.get('/stooges/stooge1') == 'Larry'
    assert cfg.get('/stooges/stooge2') == 'Curly'
    assert cfg.get('/stooges/stooge3') == 'Moe'
    assert cfg.get('/fruit') != 'banana'
    assert cfg.get('/number') == 2


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content_save(fs):
    fs.add_real_file(toml_path, False)
    cfg = SingletonSettings(application='tests', path=toml_path, writable=True)
    cfg.load()
    cfg.create('/test', 'test')
    assert cfg.settings['test'] == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    fs.add_real_file(toml_path)
    cfg = SingletonSettings(application='tests', path=toml_path)
    cfg.load()

    with pytest.raises(IOError):
        cfg.create('/test', 'test')
