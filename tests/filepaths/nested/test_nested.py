import os
import pytest  # type: ignore

from compendium.config_manager import NestedConfigManager


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_nested(fs):
    base_path = os.path.dirname(os.path.realpath(__file__))
    cfg1_path = os.path.join(os.sep, 'opt', 'test', 'fruit.toml')
    cfg2_path = os.path.join(os.sep, 'opt', 'test', 'example1', 'fruit.toml')
    cfg3_path = os.path.join(os.sep, 'opt', 'test', 'example2', 'fruit.toml')

    # Nested paths
    fs.add_real_file(
        source_path=os.path.join(base_path, 'fruit.toml'),
        target_path=cfg1_path
    )
    fs.add_real_file(
        source_path=os.path.join(base_path, 'fruit1.toml'),
        target_path=cfg2_path
    )
    fs.add_real_file(
        source_path=os.path.join(base_path, 'fruit2.toml'),
        target_path=cfg3_path
    )

    cfg = NestedConfigManager(
        application='test',
        merge_strategy='partition',
        filename='fruit.toml'
    )
    cfg.load_configs()

    print(cfg.filepaths)
    assert cfg1_path in cfg.filepaths
    assert cfg2_path in cfg.filepaths
    assert cfg3_path in cfg.filepaths
    assert cfg.get('/settings/[0]/filepath') == cfg1_path
    assert cfg.get('/settings/[1]/filepath') == cfg2_path
    assert cfg.get('/settings/[2]/filepath') == cfg3_path
    assert cfg.get('/**/name', cfg.get('/settings/**/fruit/drupe')) == 'peach'

    # Ensure vegatable is not in fruits
    # NOTE: Added defaults
    # with pytest.raises(KeyError):
    #     cfg.get('/settings/**/vegetable')
