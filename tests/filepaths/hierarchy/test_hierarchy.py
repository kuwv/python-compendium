import os

from compendium.settings import Settings

import pytest


def test_hierarchy(fs):
    # Setup base paths
    base_path = os.path.dirname(os.path.realpath(__file__))
    user_path = os.path.expanduser('~')

    # System path
    fs.add_real_file(
        source_path=base_path + '/settings.toml',
        target_path='/etc/tests/settings.toml'
    )

    # User path
    fs.add_real_file(
        source_path=base_path + '/tests.toml',
        target_path=user_path + '/.tests.toml'
    )
    fs.add_real_file(
        source_path=base_path + '/local.toml',
        target_path=user_path + '/.tests.d/settings.toml'
    )

    cfg = Settings(
        application='tests',
        merge_strategy='overlay',
        enable_system_paths=True,
        enable_user_paths=True
    )
    cfg.load()
    print(cfg.settings)

    assert ('/etc/tests/settings.toml') in cfg.filepaths
    assert (user_path + '/.tests.toml') in cfg.filepaths
    assert (user_path + '/.tests.d/settings.toml') in cfg.filepaths

    assert cfg.get('.table.subtable.key') == 'local'
    assert cfg.get('.table.subtable.key') != 'another value'

    # Ensure /etc/tests/settings.toml is blank
    with pytest.raises(KeyError) as key_error:
        cfg.get('.table.key')
