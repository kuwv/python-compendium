# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Simple configuration management tool.'''

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = ['Cache', 'ConfigPaths', 'ConfigManager', 'Settings']
