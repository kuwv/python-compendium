# -*- coding: utf-8 -*-
import logging
import os
from logging.config import dictConfig
from pprint import pformat


class Logger(object):

    log = None
    log_format = '%(levelname)s - %(name)s:%(lineno)d — %(message)s'
    time_log_format = '%(asctime)s — {l}'.format(l=log_format)

    # def __init__(self, module_name: str = None, *sp: str, **svc_args: str):
    def __init__(self, module_name, settings_object=None):
        if settings_object is not None:
            dictConfig(settings_object.get_settings())

        self.log = logging.getLogger(module_name)
        # self.setupConsole(loglevel='DEBUG')
        # self.setupLogfile(loglevel='DEBUG')
        self.log.info('Lunar logging setup complete')

    def __setFormat(self, logformat: str):
        return logging.Formatter(logformat)

    def __setLevel(self, loglevel: str):
        if loglevel == 'DEBUG':
            return logging.DEBUG
        if loglevel == 'INFO':
            return logging.INFO
        if loglevel == 'WARNING':
            return logging.WARNING
        if loglevel == 'ERROR':
            return logging.ERROR
        if loglevel == 'CRITICAL':
            return logging.CRITICAL

    def __setHandler(self, handler: str, loglevel: str, timeformat: str):
        handler.setLevel(self.__setLevel(loglevel))
        handler.setFormatter(self.__setFormat(timeformat))
        self.log.addHandler(handler)

    # TODO: Load handlers as modules
    def setupConsole(self, loglevel: str = 'INFO', logformat: str = log_format):
        self.__setHandler(logging.StreamHandler(), loglevel, logformat)
        self.log.info('Lunar console logger setup complete')

    def setupLogfile(
        self,
        loglevel: str = 'INFO',
        logformat: str = time_log_format,
        filepath: str = os.getcwd() + '/lunar.log',
    ):
        self.__setHandler(logging.FileHandler(filepath), loglevel, logformat)
        self.log.info('Lunar file logger setup complete')

    def setupEmail(
        self,
        loglevel: str = 'INFO',
        logformat: str = time_log_format,
        email: str = 'root@localhost'
    ):
        pass

    def setup_logger(self, *sp: str, **kwargs: str):
        # TODO: Implement validation and/or config splitting
        logging.basicConfig(**kwargs)
        self.setupConsole(loglevel=kwargs.get('level'))
        self.setupLogfile(loglevel=kwargs.get('level'))
        self.log.info('Lunar logging setup complete')

    def setupLogger(self, module_name: str, settings_object: str):
        dictConfig(settings_object.get_settings())
        self.log = logging.getLogger(module_name)

    def __format(self, message: str):
        if isinstance(message, dict):
            return pformat(message)
        else:
            return message

    def debug(self, message: str):
        self.log.debug(self.__format(message))

    def info(self, message: str):
        self.log.info(self.__format(message))

    def warning(self, message: str):
        self.log.warning(self.__format(message))

    def error(self, message: str):
        self.log.exception(self.__format(message))

    def critical(self, message: str):
        self.log.critical(self.__format(message))
