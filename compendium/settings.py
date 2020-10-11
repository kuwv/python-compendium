# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide settings modules.'''

import logging
import os
from typing import Any, ClassVar, Dict, Optional

from dpath import util as dpath  # type: ignore


class Settings:
    '''Manage settings loaded from confiugrations.'''

    __defaults: ClassVar[Dict[Any, Any]] = {}
    __environs: ClassVar[Dict[Any, Any]] = {}

    def __init__(self, application: str, **kwargs):
        '''Initialize settings store.'''
        self.application = application

        self.__document: Dict[Any, Any] = {}
        self.__settings: Dict[Any, Any] = {}
        if 'defaults' in kwargs and Settings.__defaults == {}:
            Settings.__defaults = kwargs['defaults']

        # Load settings from configs
        self.separator: str = kwargs.get('separator', '/')
        self.prefix = kwargs.get('prefix', "{a}_".format(a=application.upper()))

    @property
    def defaults(self) -> Dict[Any, Any]:
        '''Return default settings.'''
        return self.__defaults

    @property
    def settings(self) -> Dict[Any, Any]:
        '''Return settings.'''
        return self.__settings

    def load_environment(self) -> None:
        '''Load environment variables.'''
        # TODO: Change env key from '_' to dict path
        env = [
            {k.replace(self.prefix, '').lower(): v}
            for k, v in os.environ.items()
            if k.startswith(self.prefix)
        ]
        if env != []:
            Settings.__environs = {'env': env}

    def _initialize_settings(self, new_settings: Dict[Any, Any]) -> None:
        '''Load settings store.'''
        logging.debug(new_settings)
        self.__settings.update(new_settings)
        self.load_environment()

    # Query
    def get(
        self,
        query: str,
        document: Optional[Dict[Any, Any]] = None,
        default: Optional[Any] = None,
    ):
        '''Get value from settings with key.'''
        if not document:
            document = self.__settings
        documents = [self.__environs, document, self.__defaults]
        for doc in documents:
            try:
                return dpath.get(doc, query, self.separator)
                break
            except KeyError:
                pass
        return default

    def retrieve(self, query: str):
        '''Retrieve value from settings with key.'''
        if not self.__document:
            self.__document = self.__settings
        self.__document = dpath.get(self.__document, query, self.separator)
        return self

    def search(self, query: str) -> Dict[Any, Any]:
        '''Search settings matching query.'''
        return dpath.values(self.__settings, query, self.separator)

    def append(self, keypath: str, value: Any) -> None:
        '''Append to a list located at keypath.'''
        store = [value]
        keypath_dir = keypath.split(self.separator)[1:]
        for x in reversed(keypath_dir):
            store = {x: store}  # type: ignore
        dpath.merge(self.__settings, store)

    def update(self, keypath: str, value: Any) -> None:
        '''Update value located at keypath.'''
        dpath.set(self.__settings, keypath, value, self.separator)

    def add(self, keypath: str, value: Any) -> None:
        '''Add key/value pair located at keypath.'''
        dpath.new(self.__settings, keypath, value, self.separator)

    def create(self, keypath: str, value: Any) -> None:
        '''Create new key/value pair located at path.'''
        dpath.new(self.__settings, keypath, value, self.separator)

    def delete(self, keypath: str) -> None:
        '''Delete key/value located at keypath.'''
        dpath.delete(self.__settings, keypath, self.separator)

    # def view(self) -> str:
    #     '''View current keypath location.'''
    #     return self.keypath
