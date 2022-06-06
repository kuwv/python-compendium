# type: ignore
"""Test tree configuration."""

import os
import pytest

from compendium.exceptions import ConfigManagerError
from compendium.config_manager import TreeConfigManager


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_tree(fs):
    base_path = os.path.dirname(os.path.realpath(__file__))
    basedir = os.path.join(os.sep, 'opt', 'test')
    cfg1_path = os.path.join(basedir, 'fruit.toml')
    cfg2_path = os.path.join(basedir, 'example1', 'fruit.toml')
    cfg3_path = os.path.join(basedir, 'example2', 'fruit.toml')

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

    cfg = TreeConfigManager(
        name='test',
        merge_strategy='partition',
        filename='fruit.toml',
        load_root=True,
        load_children=True,
        basedir=basedir,
    )

    with pytest.raises(ConfigManagerError):
        # NOTE: either set load_chilren true or call this but not both
        cfg.load_configs()

    assert cfg1_path in cfg.filepaths
    assert cfg2_path in cfg.filepaths
    assert cfg3_path in cfg.filepaths

    # TODO: filepaths aren't used this way
    # assert cfg.settings['/settings/[0]/filepath'] == cfg1_path
    # assert cfg.settings['/settings/[1]/filepath'] == cfg2_path
    # assert cfg.settings['/settings/[2]/filepath'] == cfg3_path

    # TODO add additional depth tests
    assert cfg.settings['/fruit/pome/**/name'] == 'apple'
    # assert cfg.retrieve(
    #     '/**/name', document=cfg.settings['/**/fruit/drupe']
    # ) == 'peach'

    # Ensure vegatable is not in fruits
    # NOTE: Added defaults
    # with pytest.raises(KeyError):
    #     cfg['/settings/**/vegetable']
