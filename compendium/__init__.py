'''Simple configuration management tool.'''
# -*- coding: utf-8 -*-

__author__ = 'Jesse P. Johnson'
__title__ = 'compendium'
__version__ = '0.1.1-dev58'
__license__ = 'Apache-2.0'

__all__ = ['ConfigPaths', 'ConfigManager', 'Settings']

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
