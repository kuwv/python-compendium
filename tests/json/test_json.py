import os
import pytest

from compendium.config.paths import ConfigPaths
from compendium.settings import Settings

settings_path = os.path.dirname(os.path.realpath(__file__))
json_path = settings_path + '/test.json'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_empty_filepath(fs):
    cfg = ConfigPaths(application='empty', filename='test.json')
    cfg.load_configs()
    assert not cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_json_path(fs):
    fs.add_real_file(json_path)
    cfg = ConfigPaths(application='json', filename='test.json')
    cfg.load_config_filepath(settings_path + '/test.json')
    assert "{}/test.json".format(settings_path) in cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg(fs):
    fs.add_real_file(json_path)
    cfg = Settings(application='tests', path=json_path)
    cfg.load()
    assert cfg.get('/stooges/stooge1') == 'Larry'
    assert cfg.get('/stooges/stooge2') == 'Curly'
    assert cfg.get('/stooges/stooge3') == 'Moe'
    assert cfg.get('/fruit') != 'banana'
    assert cfg.get('/number') == 2


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save(fs):
    fs.add_real_file(json_path, False)
    cfg = Settings(application='tests', path=json_path, writable=True)
    cfg.load()
    cfg.create('/test', 'test')
    assert cfg.settings['test'] == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    fs.add_real_file(json_path)
    cfg = Settings(application='tests', path=json_path)
    cfg.load()

    with pytest.raises(IOError):
        cfg.create('/test', 'test')
