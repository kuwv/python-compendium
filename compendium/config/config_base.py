# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide plugin base for configuration modules.'''
from abc import ABCMeta, abstractmethod


class ConfigBase(metaclass=ABCMeta):
    '''Define required configuration module methods.'''

    # @abstractproperty
    # def filesystems():
    #     '''Retrieve extensions of filetypes.'''

    @abstractmethod
    def load_config(self, filepath):
        '''Load configuration from file.'''

    @abstractmethod
    def save_config(self, content, filepath):
        '''Save confgration to file.'''
