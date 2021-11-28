# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Test TOML configuration management."""

import os
import pytest  # type: ignore

from compendium.loader import ConfigFile
from compendium.exceptions import CompendiumConfigFileError

config_filepath = os.path.dirname(os.path.realpath(__file__))
toml_filepath = os.path.join(config_filepath, 'test.toml')


# def test_empty_filepath():
#     """Test empty file."""
#     cfg = ConfigFile(name='empty', filename='test.toml')
#     cfg.load()
#     assert not cfg.filepath


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_filepath(fs):
    """Test TOML filepaths."""
    fs.add_real_file(toml_filepath)
    cfg = ConfigFile(
        name='toml',
        filepath=os.path.join(config_filepath, 'test.toml')
    )
    assert "{}/test.toml".format(config_filepath) == cfg.filepath


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content(fs):
    """Test TOML content load."""
    fs.add_real_file(toml_filepath)
    cfg = ConfigFile(name='tests')
    cfg.load(filepath=toml_filepath)
    assert cfg.retrieve('/stooges/stooge1') == 'Larry'
    assert cfg.retrieve('/stooges/stooge2') == 'Curly'
    assert cfg.retrieve('/stooges/stooge3') == 'Moe'
    assert cfg.retrieve('/fruit') != 'banana'
    assert cfg.retrieve('/number') == 2


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content_dump(fs):
    """Test TOML content save."""
    fs.add_real_file(toml_filepath, False)
    cfg = ConfigFile(name='tests', writable=True)
    cfg.load(filepath=toml_filepath)
    cfg.create('/test', 'test')
    # TODO where is save happening :/
    assert cfg.retrieve('test') == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    """Test TOML content failure."""
    fs.add_real_file(toml_filepath)
    cfg = ConfigFile(name='tests')
    cfg.load(filepath=toml_filepath)

    with pytest.raises(CompendiumConfigFileError):
        cfg.create('/test', 'test')
        cfg.dump('./test.toml')
