# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Simple configuration management tool."""

import logging

__author__ = 'Jesse P. Johnson'
__author_email__ = 'jpj6652@gmail.com'
__title__ = 'compendium'
__description__ = 'Inspection based parser built on argparse.'
__version__ = '0.1.1-a3'
__license__ = 'Apache-2.0'
__copyright__ = 'Copyright 2020 Jesse Johnson.'
__all__ = [
    'ConfigFile',
    'ConfigPaths',
    'HierarchyConfigManager',
    'TreeConfigManager',
    'Settings',
]

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
