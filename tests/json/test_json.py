# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
# type: ignore
"""Test JSON content management."""

import os
import pytest

from compendium.loader import ConfigFile
from compendium.exceptions import CompendiumConfigFileError

settings_filepath = os.path.dirname(os.path.realpath(__file__))
json_filepath = os.path.join(settings_filepath, 'test.json')


# @pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
# def test_empty_filepath(fs):
#     """Test empty file."""
#     cfg = ConfigPaths(name='empty')
#     cfg.load_configs(filename='test.json')
#     assert not cfg.filepaths


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_json_filepath(fs):
    """Test JSON filepaths."""
    fs.add_real_file(json_filepath)
    cfg = ConfigFile(
        name='json',
        filepath=os.path.join(settings_filepath, 'test.json'),
    )
    assert "{}/test.json".format(settings_filepath) == cfg.filepath


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg(fs):
    """Test loading JSON configuration."""
    fs.add_real_file(json_filepath)
    cfg = ConfigFile(name='tests')
    cfg.load(filepath=json_filepath)
    assert cfg.retrieve('/stooges/stooge1') == 'Larry'
    assert cfg.retrieve('/stooges/stooge2') == 'Curly'
    assert cfg.retrieve('/stooges/stooge3') == 'Moe'
    assert cfg.retrieve('/fruit') != 'banana'
    assert cfg.retrieve('/number') == 2


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_dump(fs):
    """Test saving JSON content."""
    fs.add_real_file(json_filepath, False)
    cfg = ConfigFile(name='tests', writable=True)
    cfg.load(filepath=json_filepath)
    cfg.create('/test', 'test')
    assert cfg.retrieve('test') == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_cfg_save_fail(fs):
    """Test JSON failure."""
    fs.add_real_file(json_filepath)
    cfg = ConfigFile(name='tests')
    cfg.load(filepath=json_filepath)

    with pytest.raises(CompendiumConfigFileError):
        cfg.create('/test', 'test')
        cfg.dump('./test.json')
