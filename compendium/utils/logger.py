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
        self.application = 'compendium'

        if settings_object is not None:
            dictConfig(settings_object.get_settings())

        self.log = logging.getLogger(module_name)
        # self.setupConsole(loglevel='DEBUG')
        # self.setupLogfile(loglevel='DEBUG')
        self.log.info('Lunar logging setup complete')

    def __set_format(self, logformat: str):
        return logging.Formatter(logformat)

    def __set_level(self, loglevel: str):
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

    def __set_handler(self, handler: str, loglevel: str, timeformat: str):
        handler.setLevel(self.__set_level(loglevel))
        handler.setFormatter(self.__set_format(timeformat))
        self.log.addHandler(handler)

    # TODO: Load handlers as modules
    def setup_console(
            self,
            loglevel: str = 'INFO',
            logformat: str = log_format
    ):
        self.__set_handler(logging.StreamHandler(), loglevel, logformat)
        self.log.info('Lunar console logger setup complete')

    def setup_logfile(
        self,
        loglevel: str = 'INFO',
        logformat: str = time_log_format,
        filepath: Optional[str] = None,
    ):
        if not filepath:
            filepath = os.getcwd() + '/' + self.application + '.log'
        self.__setHandler(logging.FileHandler(filepath), loglevel, logformat)
        self.log.info('Lunar file logger setup complete')

    def setup_email(
        self,
        loglevel: str = 'INFO',
        logformat: str = time_log_format,
        email: str = 'root@localhost'
    ):
        pass

    def _setup_logger(self, *sp: str, **kwargs: str):
        # TODO: Implement validation and/or config splitting
        logging.basicConfig(**kwargs)
        self.setup_console(loglevel=kwargs.get('level'))
        self.setup_logfile(loglevel=kwargs.get('level'))
        self.log.info('logging setup complete')

    def setup_logger(self, module_name: str, settings_object: str):
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
