# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class ConfigBase(metaclass=ABCMeta):
    # @abstractproperty
    # def filesystems():
    #     '''Retrieve extensions of filetypes'''

    @abstractmethod
    def load_config(self, filepath):
        '''Load configuration from file'''

    @abstractmethod
    def save_config(self):
        '''Save confgration to file'''

class ConfigMixin:
    def update_config(self, content):
        '''Apply update to config'''
        self._configuration = content

    def get_config(self):
        '''Get configuration as dictionary'''
        return self._configuration
