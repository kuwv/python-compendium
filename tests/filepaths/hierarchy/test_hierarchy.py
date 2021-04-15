import os

from compendium.config_manager import HierarchyConfigManager

import pytest  # type: ignore


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_hierarchy(fs):
    # Setup base paths
    base_filepath = os.path.dirname(os.path.realpath(__file__))
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
        target_path=os.path.join(global_filepath, '.hierarchy.d', 'config.toml')
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

    assert cfg.settings.retrieve('/table/key') != 'first'  # overridden
    assert cfg.settings.retrieve('/table/subtable/key') == 'third'
    assert cfg.settings.retrieve(
        '/table/subtable/second'
    ) != 'retained'  # overridden
    assert cfg.settings.retrieve('/table/subtable/third') == 'retained'
    assert cfg.settings.retrieve('/table/subtable/key') != 'second'
    assert cfg.settings.retrieve('/list/**/last') == 'third'

    # Ensure /etc/hierarchy/config.toml is blank
    # NOTE: Added default
    # with pytest.raises(KeyError):
    #     cfg.retrieve('/list/**/overwritten1')
    #     cfg.retrieve('/list/**/overwritten2')
