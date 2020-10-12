# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Simple configuration management tool.'''

import logging

__all__ = ['Cache', 'ConfigPaths', 'ConfigManager', 'Settings']

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
