# -*- coding: utf-8 -*-
'''Simple configuration management tool'''

__title__ = 'compendium'
__version__ = '0.1.1-dev9'
__license__ = 'Apache-2.0'

__all__ = ['ConfigPaths', 'ConfigManager', 'Settings']

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
