# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
# type: ignore
"""Test TOML configuration management."""

import os
import pytest

from compendium.loader import ConfigFile
from compendium.exceptions import CompendiumConfigFileError

config_filepath = os.path.dirname(os.path.realpath(__file__))
ini_filepath = os.path.join(config_filepath, 'test.ini')


# def test_empty_filepath():
#     """Test empty file."""
#     cfg = ConfigFile(name='empty', filename='test.ini')
#     cfg.load()
#     assert not cfg.filepath


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_ini_filepath(fs):
    """Test TOML filepaths."""
    fs.add_real_file(ini_filepath)
    cfg = ConfigFile(
        name='ini',
        filepath=os.path.join(config_filepath, 'test.ini')
    )
    assert "{}/test.ini".format(config_filepath) == cfg.filepath


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_ini_content(fs):
    """Test TOML content load."""
    fs.add_real_file(ini_filepath)
    cfg = ConfigFile(name='tests')
    cfg.load(filepath=ini_filepath)
    assert cfg.retrieve('/stooges/stooge1') == 'Larry'
    assert cfg.retrieve('/stooges/stooge2') == 'Curly'
    assert cfg.retrieve('/stooges/stooge3') == 'Moe'
    assert cfg.retrieve('/fruit') == 'apple'
    assert int(cfg.retrieve('/number')) == 2


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_ini_content_dump(fs):
    """Test TOML content save."""
    fs.add_real_file(ini_filepath, False)
    cfg = ConfigFile(name='tests', writable=True)
    cfg.load(filepath=ini_filepath)
    cfg.create('/test', 'test')
    # TODO where is save happening :/
    assert cfg.retrieve('test') == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    """Test TOML content failure."""
    fs.add_real_file(ini_filepath)
    cfg = ConfigFile(name='tests')
    cfg.load(filepath=ini_filepath)

    with pytest.raises(CompendiumConfigFileError):
        cfg.create('/test', 'test')
        cfg.dump('./test.ini')
