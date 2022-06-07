# type: ignore
"""Test hierarchial configuration."""

import os

from compendium.config_manager import HierarchyConfigManager

import pytest


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_hierarchy(fs):
    # Setup base paths
    base_filepath = os.path.dirname(__file__)
    global_filepath = os.path.expanduser('~')

    # System path
    fs.add_real_file(
        source_path=os.path.join(base_filepath, 'settings1.toml'),
        target_path=os.path.join(os.sep, 'etc', 'hierarchy', 'config.toml')
    )

    # User path
    fs.add_real_file(
        source_path=os.path.join(base_filepath, 'settings2.toml'),
        target_path=os.path.join(global_filepath, '.hierarchy.toml')
    )
    fs.add_real_file(
        source_path=os.path.join(base_filepath, 'settings3.toml'),
        target_path=os.path.join(
            global_filepath, '.hierarchy.d', 'config.toml'
        )
    )

    cfg = HierarchyConfigManager(
        name='hierarchy',
        filename='config.toml',
        merge_strategy='overlay',
        enable_system_filepaths=True,
        enable_global_filepaths=True
    )
    cfg.load_configs()

    assert (
        os.path.join(os.sep, 'etc', 'hierarchy', 'config.toml')
    ) in cfg.filepaths
    assert (os.path.join(global_filepath, '.hierarchy.toml')) in cfg.filepaths
    assert (
        os.path.join(global_filepath, '.hierarchy.d', 'config.toml')
    ) in cfg.filepaths

    assert cfg.data['/table/key'] != 'first'  # overridden
    assert cfg.data['/table/subtable/key'] == 'third'
    assert cfg.data['/table/subtable/second'] == 'retained'
    assert cfg.data['/table/subtable/third'] == 'retained'
    assert cfg.data['/table/subtable/key'] != 'second'
    assert cfg.data['/list/**/last'] == 'third'

    with pytest.raises(KeyError):
        cfg.data['/list/**/overwritten1']
        cfg.data['/list/**/overwritten2']

    # TODO: test clear
    # assert cfg.data is not None
    # cfg.data.clear()
    # assert cfg.data is None
