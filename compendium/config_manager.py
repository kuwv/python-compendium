# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide configuration manager for multiple settings.'''

import logging
import os
from multiprocessing import Manager, Process
from typing import List, Optional, Union

from .cache import SettingsCache


class ConfigManager:
    '''Manage multiple disperate settings groups.'''

    def __init__(self, *args, **kwargs):
        '''Inialize configuration manager.'''
        self.procs: list = []

        self.application = kwargs.get('application')
        configs = kwargs.get('configs')

        manager = Manager()
        for config in configs:
            c = manager.dict(config)
            p = Process(
                target=self.add_config,
                args=(c,)
            )
            self.procs.append(p)
            p.start()

    def add_config(self, config: dict):
        '''Add configuration cache to manage.'''
        print(config)
        # return SettingsCache(self.application, **config).load()

    def stop_all(self):
        for proc in self.procs:
            print(proc)
            proc.join()
