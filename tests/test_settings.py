# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
# type: ignore
"""Test settings management."""

import os

import pytest

from compendium.loader import ConfigFile

basedir = os.path.dirname(__file__)
filepath = os.path.join(basedir, 'config.toml')


# @pytest.fixture(params=['fs', [[['pkgutil']]]])
# def cfg(fs):
#     fs.add_real_file(filepath, False)
#     cfg = ConfigFile(filepath)
#     settings = cfg.load()
#     return settings
#
# def test_result(cfg):
#     result = settings.values('/servers/**/ip')
#     assert ['10.0.0.1', '10.0.0.2'] == result


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_result(fs):
    """Test IP from settings."""
    fs.add_real_file(filepath, False)
    cfg = ConfigFile(filepath)
    settings = cfg.load()
    result = settings.values('/servers/**/ip')
    for x in ['10.0.0.1', '10.0.0.2']:
        assert x in result


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content_create(fs):
    """Test content creation settings."""
    fs.add_real_file(filepath, False)
    cfg = ConfigFile(filepath)
    settings = cfg.load()
    settings['/test'] = 'test'
    assert settings.lookup('test') == 'test'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content_append(fs):
    """Test appending settings to list."""
    fs.add_real_file(filepath, False)
    cfg = ConfigFile(filepath)
    settings = cfg.load()
    settings.append('/database/ports', 2345)
    assert 2345 in settings.lookup('/database/ports')


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_content_update(fs):
    """Test content update."""
    fs.add_real_file(filepath, False)
    cfg = ConfigFile(filepath, writable=True)
    settings = cfg.load()
    settings['/owner/name'] = 'Tom Waits'
    assert settings.lookup('/owner/name') == 'Tom Waits'


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_delete(fs):
    """Test content deletion."""
    fs.add_real_file(filepath, False)
    cfg = ConfigFile(filepath)
    settings = cfg.load()
    assert settings.values('/owner/name') == ['Tom Preston-Werner']
    del settings['/owner/name']
    assert settings.values('/owner/name') == []
