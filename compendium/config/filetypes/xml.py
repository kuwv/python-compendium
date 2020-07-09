# -*- coding: utf-8 -*-
# import datetime
import errno
import logging
import os
import xmltodict  # type: ignore

from .. import ConfigBase


class XmlConfig(ConfigBase):
    def __init__(self, **kwargs):
        logging.info('Inializing XmlConfig')
        self.encoding = kwargs.get('encoding', 'utf-8')
        self.encoder = kwargs.get('encoder', str)
        self.process_namespaces = kwargs.get('process_namespaces', False)
        self.namespaces = kwargs.get('namespaces', None)

    @staticmethod
    def filetypes():
        return ['xml']

    def load_config(self, filepath):
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
