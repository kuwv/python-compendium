import os

from compendium.settings import HierarchySettings

import pytest


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_hierarchy(fs):
    # Setup base paths
    base_path = os.path.dirname(os.path.realpath(__file__))
    user_path = os.path.expanduser('~')

    # System path
    fs.add_real_file(
        source_path=base_path + '/settings1.toml',
        target_path='/etc/tests/settings.toml'
    )

    # User path
    fs.add_real_file(
        source_path=base_path + '/settings2.toml',
        target_path=user_path + '/.tests.toml'
    )
    fs.add_real_file(
        source_path=base_path + '/settings3.toml',
        target_path=user_path + '/.tests.d/settings.toml'
    )

    cfg = HierarchySettings(
        application='tests',
        merge_strategy='overlay',
        enable_system_paths=True,
        enable_user_paths=True
    )
    cfg.load()

    assert ('/etc/tests/settings.toml') in cfg.filepaths
    assert (user_path + '/.tests.toml') in cfg.filepaths
    assert (user_path + '/.tests.d/settings.toml') in cfg.filepaths

    assert cfg.get('/table/key') == 'first'
    assert cfg.get('/table/subtable/key') == 'third'
    assert cfg.get('/table/subtable/second') == 'retained'
    assert cfg.get('/table/subtable/third') == 'retained'
    assert cfg.get('/table/subtable/key') != 'second'
    assert cfg.get('/list/**/last') == 'third'

    # Ensure /etc/tests/settings.toml is blank
    with pytest.raises(KeyError):
        cfg.get('/list/**/overwritten1')
        cfg.get('/list/**/overwritten2')
