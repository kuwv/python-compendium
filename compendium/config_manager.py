# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide configuration manager for multiple settings.'''

# import logging
# import os
# from typing import List, Optional, Union

# from multiprocessing import Process

from .settings import Settings


class ConfigManager:
    '''Manage multiple disperate settings groups.'''

    def __init__(self, *args, **kwargs):

        for config in kwargs.get('configs'):
            self.add_config(config)

    def add_config(self, config: dict):
        self.configs.append({config['application']: Settings(**config)})
        self.configs[config['application']].load()
