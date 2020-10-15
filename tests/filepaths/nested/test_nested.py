import os
import pytest  # type: ignore

from compendium.config_manager import NestedConfigManager


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_nested(fs):
    base_path = os.path.dirname(os.path.realpath(__file__))

    # Nested paths
    fs.add_real_file(
        source_path=os.path.join(base_path, 'fruit.toml'),
        target_path=os.path.join(os.sep, 'opt', 'test', 'fruit.toml')
    )
    fs.add_real_file(
        source_path=os.path.join(base_path, 'fruit1.toml'),
        target_path=os.path.join(
            os.sep, 'opt', 'test', 'example1', 'fruit.toml'
        )
    )
    fs.add_real_file(
        source_path=os.path.join(base_path, 'fruit2.toml'),
        target_path=os.path.join(
            os.sep, 'opt', 'test', 'example2', 'fruit.toml'
        )
    )

    cfg = NestedConfigManager(application='test', merge_strategy='partition')
    cfg.load_configs()

    assert (os.path.join(os.sep, 'opt', 'test', 'fruit.toml')) in cfg.filepaths
    assert (
        os.path.join(os.sep, 'opt', 'test', 'example1', 'fruit.toml')
    ) in cfg.filepaths
    assert (
        os.path.join(os.sep, 'opt', 'test', 'example2', 'fruit.toml')
    ) in cfg.filepaths
    assert cfg.get('/settings/[0]/filepath') == '/opt/test/fruit.toml'
    assert cfg.get('/settings/[1]/filepath') == '/opt/test/example1/fruit.toml'
    assert cfg.get('/settings/[2]/filepath') == '/opt/test/example2/fruit.toml'
    assert cfg.get('/**/name', cfg.get('/settings/**/fruit/drupe')) == 'peach'

    # Ensure vegatable is not in fruits
    # NOTE: Added defaults
    # with pytest.raises(KeyError):
    #     cfg.get('/settings/**/vegetable')
