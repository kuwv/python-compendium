'''Control XML module.'''
# -*- coding: utf-8 -*-
# import datetime
import errno
import logging
import os
import xmltodict  # type: ignore

from .. import ConfigBase


class XmlConfig(ConfigBase):
    '''Manage XML configurations.'''

    def __init__(self, **kwargs):
        '''Initialize XML configuration module.'''
        logging.info('Inializing XmlConfig')
        self.encoding = kwargs.get('encoding', 'utf-8')
        self.encoder = kwargs.get('encoder', str)
        self.process_namespaces = kwargs.get('process_namespaces', False)
        self.namespaces = kwargs.get('namespaces', None)

    @staticmethod
    def filetypes():
        '''Return supported XML configuration filetypes.'''
        return ['xml']

    def load_config(self, filepath):
        '''Load settings from XML configuration.'''
        logging.info('XmlConfig: loading configuration file')
        if os.path.isfile(filepath):
            with open(filepath, 'r') as f:
                content = xmltodict.parse(
                    f.read(),
                    encoding=self.encoding,
                    process_namespaces=self.process_namespaces,
                    namespaces=self.namespaces
                )
        else:
            content = {}
        return content

    def save_config(self, content, filepath):
        '''Save settings to XML configuration.'''
        try:
            with open(filepath, 'w') as f:
                f.write(
                    xmltodict.unparse(
                        content,
                        encoding=self.encoding,
                        pretty=True
                    )
                )
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'Error: You do not have permission to write to this file'
                )
                raise
