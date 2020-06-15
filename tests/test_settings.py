import os

from compendium.settings import Settings

config_path = os.path.dirname(os.path.realpath(__file__))
settings_path = config_path + '/settings.toml'


def test_query():
    content = Settings(application='tests', path=settings_path)
    content.load()
    query = content.search('.servers.**.ip')
    assert ['10.0.0.1', '10.0.0.2'] == query


def test_toml_content_create(fs):
    fs.add_real_file(settings_path, False)
    settings = Settings(application='tests', path=settings_path)
    settings.load()
    settings.create('.test', 'test')
    assert settings.get('test') == 'test'


def test_toml_content_update(fs):
    fs.add_real_file(settings_path, False)
    settings = Settings(application='tests', path=settings_path)
    settings.load()
    settings.update('.owner.name', 'Tom Waits')
    assert settings.get('.owner.name') == 'Tom Waits'


def test_toml_delete(fs):
    fs.add_real_file(settings_path, False)
    content = Settings(application='tests', path=settings_path)
    content.load()
    assert content.search('.owner.name') == ['Tom Preston-Werner']
    content.delete('.owner.name')
    assert content.search('.owner.name') == []
