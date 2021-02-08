import os

from compendium.config_manager import HierarchyConfigManager

import pytest  # type: ignore


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_hierarchy(fs):
    # Setup base paths
    base_filepath = os.path.dirname(os.path.realpath(__file__))
    user_filepath = os.path.expanduser('~')

    # System path
    fs.add_real_file(
        source_path=os.path.join(base_filepath, 'settings1.toml'),
        target_path=os.path.join(os.sep, 'etc', 'tests', 'settings.toml')
    )

    # User path
    fs.add_real_file(
        source_path=os.path.join(base_filepath, 'settings2.toml'),
        target_path=os.path.join(user_filepath, '.tests.toml')
    )
    fs.add_real_file(
        source_path=os.path.join(base_filepath, 'settings3.toml'),
        target_path=os.path.join(user_filepath, '.tests.d', 'settings.toml')
    )

    cfg = HierarchyConfigManager(
        application='tests',
        merge_strategy='overlay',
        enable_system_filepaths=True,
        enable_user_filepaths=True
    )
    cfg.load_configs()

    assert (
        os.path.join(os.sep, 'etc', 'tests', 'settings.toml')
    ) in cfg.filepaths
    assert (os.path.join(user_filepath, '.tests.toml')) in cfg.filepaths
    assert (
        os.path.join(user_filepath, '.tests.d', 'settings.toml')
    ) in cfg.filepaths

    assert cfg.settings.get('/table/key') == 'first'
    assert cfg.settings.get('/table/subtable/key') == 'third'
    assert cfg.settings.get('/table/subtable/second') == 'retained'
    assert cfg.settings.get('/table/subtable/third') == 'retained'
    assert cfg.settings.get('/table/subtable/key') != 'second'
    assert cfg.settings.get('/list/**/last') == 'third'

    # Ensure /etc/tests/settings.toml is blank
    # NOTE: Added default
    # with pytest.raises(KeyError):
    #     cfg.settings.get('/list/**/overwritten1')
    #     cfg.settings.get('/list/**/overwritten2')
