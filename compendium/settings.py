# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide settings modules.'''

import logging
import os
from collections import UserDict
from typing import Any, ClassVar, Dict, Optional

from dpath import util as dpath  # type: ignore


class Settings(UserDict):
    '''Manage settings loaded from confiugrations.'''

    __defaults: ClassVar[Dict[Any, Any]] = {}
    __environs: ClassVar[Dict[Any, Any]] = {}

    def __init__(self, application: str, **kwargs):
        '''Initialize settings store.'''
        self.application = application

        self.__document: Dict[Any, Any] = {}

        if 'defaults' in kwargs and Settings.__defaults == {}:
            Settings.__defaults = kwargs['defaults']

        # Load settings from configs
        self.prefix = kwargs.get('prefix', "{a}_".format(a=application.upper()))
        self.__separator: str = kwargs.pop('separator', '/')

        super().__init__(**kwargs)
        print('data', self.data)

    def __repr__(self) -> str:
        '''Get string representaion.'''
        return f"{self.data}"

    # def __getattr__(self, k: str) -> str:
    #     print('this is the args', k)
    #     return self.data[k]

    # def __setattr__(self, k: str, v: Any) -> None:
    #     self.data[k] = v

    @property
    def defaults(self) -> Dict[Any, Any]:
        '''Return default settings.'''
        return self.__defaults

    @property
    def settings(self) -> Dict[Any, Any]:
        '''Return settings.'''
        return self.data

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
        self.data.update(new_settings)
        self.load_environment()

    # Query
    def get(
        self,
        query: str,
        default: Optional[Any] = None,
        document: Optional[Dict[Any, Any]] = None,
    ):
        '''Get value from settings with key.'''
        if not document:
            document = self.data
        documents = [self.__environs, document, self.__defaults]
        for doc in documents:
            try:
                return dpath.get(doc, query, self.__separator)
                break
            except KeyError:
                pass
        return default

    def retrieve(self, query: str):
        '''Retrieve value from settings with key.'''
        if not self.__document:
            self.__document = self.data
        self.__document = dpath.get(self.__document, query, self.__separator)
        return self

    def search(self, query: str) -> Dict[Any, Any]:
        '''Search settings matching query.'''
        return dpath.values(self.data, query, self.__separator)

    def append(self, keypath: str, value: Any) -> None:
        '''Append to a list located at keypath.'''
        store = [value]
        keypath_dir = keypath.split(self.__separator)[1:]
        for x in reversed(keypath_dir):
            store = {x: store}  # type: ignore
        dpath.merge(self.data, store)

    def set(self, keypath: str, value: Any) -> None:
        '''Update value located at keypath.'''
        dpath.set(self.data, keypath, value, self.__separator)

    def add(self, keypath: str, value: Any) -> None:
        '''Add key/value pair located at keypath.'''
        dpath.new(self.data, keypath, value, self.__separator)

    def create(self, keypath: str, value: Any) -> None:
        '''Create new key/value pair located at path.'''
        dpath.new(self.data, keypath, value, self.__separator)

    def delete(self, keypath: str) -> None:
        '''Delete key/value located at keypath.'''
        dpath.delete(self.data, keypath, self.__separator)

    def merge(self, document: Optional[Dict[Any, Any]] = None):
        '''Merge document.'''
        dpath.merge(self.data, document, flags=2)

    # def view(self) -> str:
    #     '''View current keypath location.'''
    #     return self.keypath

    # print
    # map
    # readlines
    # filter
    # find
    # findall
    # each
    # len
    # all
