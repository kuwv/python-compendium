# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import os


class ConfigBase(metaclass=ABCMeta):
    _configuration = {}

    @abc.abstractproperty
    def filesystems(self):
        """Retrieve extensions of filetypes"""
        return 'Extensions of filetypes'

    @abstractmethod
    def load_config(self, filepath):
        """Load configuration from file"""

    @abstractmethod
    def save_config(self):
        """Save confgration to file"""

    @classmethod
    def update_config(cls, content):
        """Apply update to config"""
        cls._configuration.update(content)

    @classmethod
    def get_config(cls):
        """Get configuration as dictionary"""
        return cls._configuration
