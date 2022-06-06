# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Simple configuration management tool."""

import logging

from compendium.config_manager import (  # noqa
    ConfigManager,
    HierarchyConfigManager,
    TreeConfigManager,
)
from compendium.loader import ConfigFile  # noqa
from compendium.settings import Settings, SettingsMap  # noqa

__author__ = 'Jesse P. Johnson'
__author_email__ = 'jpj6652@gmail.com'
__title__ = 'compendium'
__description__ = 'Inspection based parser built on argparse.'
__version__ = '0.1.1b1'
__license__ = 'Apache-2.0'
__copyright__ = 'Copyright 2020 Jesse Johnson.'
__all__ = [
    'ConfigFile',
    'ConfigManager',
    'HierarchyConfigManager',
    'TreeConfigManager',
    'Settings',
    'SettingsMap',
]

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
