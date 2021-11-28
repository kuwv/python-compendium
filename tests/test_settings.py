# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
"""Test settings management."""

import os

import pytest  # type: ignore

from compendium.loader import ConfigFile

config_filepath = os.path.dirname(os.path.realpath(__file__))
settings_filepath = os.path.join(config_filepath, 'config.toml')


# @pytest.fixture(params=['fs', [[['pkgutil']]]])
# def cfg(fs):
#     fs.add_real_file(settings_filepath, False)
#     cfg = ConfigFile(name='tests', filepath=settings_filepath)
#     cfg.load()
#     return cfg
#
# def test_result(cfg):
#     result = cfg.search('/servers/**/ip')
#     assert ['10.0.0.1', '10.0.0.2'] == result


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_result(fs):
    """Test IP from settings."""
    fs.add_real_file(settings_filepath, False)
    cfg = ConfigFile(name='tests')
    cfg.load(settings_filepath)
    result = cfg.search('/servers/**/ip')
    assert ['10.0.0.1', '10.0.0.2'] == result


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content_create(fs):
    """Test content creation settings."""
    fs.add_real_file(settings_filepath, False)
    cfg = ConfigFile(name='tests')
    cfg.load(filepath=settings_filepath)
    cfg.create('/test', 'test')
    assert cfg.retrieve('test') == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content_append(fs):
    """Test appending settings to list."""
    fs.add_real_file(settings_filepath, False)
    cfg = ConfigFile(name='tests')
    cfg.load(filepath=settings_filepath)
    cfg.append('/database/ports', 2345)
    assert 2345 in cfg.retrieve('/database/ports')


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content_update(fs):
    """Test content update."""
    fs.add_real_file(settings_filepath, False)
    cfg = ConfigFile(name='tests', writable=True)
    cfg.load(filepath=settings_filepath)
    cfg.set('/owner/name', 'Tom Waits')
    assert cfg.retrieve('/owner/name') == 'Tom Waits'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_delete(fs):
    """Test content deletion."""
    fs.add_real_file(settings_filepath, False)
    cfg = ConfigFile(name='tests')
    cfg.load(filepath=settings_filepath)
    assert cfg.search('/owner/name') == ['Tom Preston-Werner']
    cfg.delete('/owner/name')
    assert cfg.search('/owner/name') == []
