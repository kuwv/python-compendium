# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import os


class ConfigBase(metaclass=ABCMeta):
    _configuration = {}

    @abstractmethod
    def load_conf(self, filepath):
        """ Load configuration from file """

    @abstractmethod
    def save_conf(self):
        """ Save confgration to file """

    @classmethod
    def update_conf(cls, content):
        """ Apply update to config """
        cls._configuration.update(content)

    @classmethod
    def get_conf(cls):
        """ Get configuration as dictionary """
        return cls._configuration
