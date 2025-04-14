# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
# type: ignore
"""Test version management."""

from compendium import __version__


def test_version():
    """Test project version is managed."""
    assert __version__ == '0.1.4'
