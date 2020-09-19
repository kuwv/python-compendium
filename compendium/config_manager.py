# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide configuration manager for multiple settings.'''

import logging
import os
from typing import List, Optional, Union

import multiprocessing

from .cache import SettingsCache


def worker():
    '''worker function'''
    print('Worker')
    return


class ConfigManager:
    '''Manage multiple disperate settings groups.'''

    def __init__(self, *args, **kwargs):
        '''Inialize configuration manager.'''
        self.caches: list = []

        self.application = kwargs.get('application')
        configs = kwargs.get('configs')
        for config in configs:
            p = multiprocessing.Process(target=worker)
            self.caches.append(p)
            # self.caches.append({
            #     config['filename'], self.add_config(config)
            # })
            p.start()

    def add_config(self, config: dict):
        '''Add configuration cache to manage.'''
        return SettingsCache(self.application, **config).load()
