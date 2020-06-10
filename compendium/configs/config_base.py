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
    def save_config(self, content, filepath):
        '''Save confgration to file'''
