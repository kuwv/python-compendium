import os

from compendium.settings import Settings

config_path = os.path.dirname(os.path.realpath(__file__))


def test_query():
    content = Settings(application="tests", path=config_path + "/settings.toml")
    query = content.compile("servers.*.ip")
    assert ["10.0.0.1", "10.0.0.2"] == query.search(content.settings)
