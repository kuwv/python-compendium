import os

from compendium.settings import Settings
import json


def test_nested(fs):
    base_path = os.path.dirname(os.path.realpath(__file__))

    # Nested paths
    fs.add_real_file(
        source_path=base_path + '/fruit.toml',
        target_path='/opt/test/fruit.toml'
    )
    fs.add_real_file(
        source_path=base_path + '/fruit1.toml',
        target_path='/opt/test/example1/fruit.toml'
    )
    fs.add_real_file(
        source_path=base_path + '/fruit2.toml',
        target_path='/opt/test/example2/fruit.toml'
    )

    cfg = Settings(
        application='test',
        filename='fruit.toml',
        merge_strategy='partition'
    )
    cfg.load('/opt/test/fruit.toml')
    print(cfg.filepaths)
    print(json.dumps(cfg.settings, indent=2, sort_keys=True))

    assert ('/opt/test/fruit.toml') in cfg.filepaths
    assert ('/opt/test/example1/fruit.toml') in cfg.filepaths
    assert ('/opt/test/example2/fruit.toml') in cfg.filepaths
