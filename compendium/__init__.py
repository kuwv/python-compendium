# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Simple configuration management tool.'''

__author__ = 'Jesse P. Johnson'
__title__ = 'compendium'
__version__ = '0.1.1-dev63'
__license__ = 'Apache-2.0'

__all__ = ['ConfigPaths', 'ConfigManager', 'Settings']

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
