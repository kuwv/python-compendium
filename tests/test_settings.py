import os

from compendium.settings import Settings

config_path = os.path.dirname(os.path.realpath(__file__))
settings_path = config_path + '/settings.toml'


def test_result(fs):
    fs.add_real_file(settings_path, False)
    cfg = Settings(application='tests', path=settings_path)
    cfg.load()
    result = cfg.search('/servers/**/ip')
    assert ['10.0.0.1', '10.0.0.2'] == result


def test_toml_content_create(fs):
    fs.add_real_file(settings_path, False)
    cfg = Settings(application='tests', path=settings_path)
    cfg.load()
    cfg.create('/test', 'test')
    assert cfg.get('test') == 'test'


def test_toml_content_append(fs):
    fs.add_real_file(settings_path, False)
    cfg = Settings(application='tests', path=settings_path)
    cfg.load()
    cfg.append('/database/ports', 2345)
    assert 2345 in cfg.get('/database/ports')


def test_toml_content_update(fs):
    fs.add_real_file(settings_path, False)
    cfg = Settings(application='tests', path=settings_path, writable=True)
    cfg.load()
    cfg.update('/owner/name', 'Tom Waits')
    assert cfg.get('/owner/name') == 'Tom Waits'


def test_toml_delete(fs):
    fs.add_real_file(settings_path, False)
    cfg = Settings(application='tests', path=settings_path)
    cfg.load()
    assert cfg.search('/owner/name') == ['Tom Preston-Werner']
    cfg.delete('/owner/name')
    assert cfg.search('/owner/name') == []
