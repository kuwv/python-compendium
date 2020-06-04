# -*- coding: utf-8 -*-
from pprint import pformat
import os
import logging
from logging.config import dictConfig


class Logger(object):

    log = None
    log_format = "%(levelname)s - %(name)s:%(lineno)d — %(message)s"
    time_log_format = "%(asctime)s — {l}".format(l=log_format)

    # def __init__(self, moduleName=None, *sp, **svc_args):
    def __init__(self, moduleName, settingsObj=None):
        if settingsObj is not None:
            dictConfig(settingsObj.get_settings())

        self.log = logging.getLogger(moduleName)
        # self.setupConsole(loglevel='DEBUG')
        # self.setupLogfile(loglevel='DEBUG')
        self.log.info("Lunar logging setup complete")

    def __setFormat(self, logformat):
        return logging.Formatter(logformat)

    def __setLevel(self, loglevel):
        if loglevel == "DEBUG":
            return logging.DEBUG
        if loglevel == "INFO":
            return logging.INFO
        if loglevel == "WARNING":
            return logging.WARNING
        if loglevel == "ERROR":
            return logging.ERROR
        if loglevel == "CRITICAL":
            return logging.CRITICAL

    def __setHandler(self, handler, loglevel, timeformat):
        handler.setLevel(self.__setLevel(loglevel))
        handler.setFormatter(self.__setFormat(timeformat))
        self.log.addHandler(handler)

    # TODO: Load handlers as modules
    def setupConsole(self, loglevel="INFO", logformat=log_format):
        self.__setHandler(logging.StreamHandler(), loglevel, logformat)
        self.log.info("Lunar console logger setup complete")

    def setupLogfile(
        self,
        loglevel="INFO",
        logformat=time_log_format,
        filepath=os.getcwd() + "/lunar.log",
    ):
        self.__setHandler(logging.FileHandler(filepath), loglevel, logformat)
        self.log.info("Lunar file logger setup complete")

    def setupEmail(
        self,
        loglevel="INFO",
        logformat=time_log_format,
        email="root@localhost"
    ):
        pass

    def setup_logger(self, *sp, **kwargs):
        # TODO: Implement validation and/or config splitting
        logging.basicConfig(**kwargs)
        self.setupConsole(loglevel=kwargs.get("level"))
        self.setupLogfile(loglevel=kwargs.get("level"))
        self.log.info("Lunar logging setup complete")

    def setupLogger(self, moduleName, settingsObj):
        dictConfig(settingsObj.get_settings())
        self.log = logging.getLogger(moduleName)

    def __format(self, message):
        if isinstance(message, dict):
            return pformat(message)
        else:
            return message

    def debug(self, message):
        self.log.debug(self.__format(message))

    def info(self, message):
        self.log.info(self.__format(message))

    def warning(self, message):
        self.log.warning(self.__format(message))

    def error(self, message):
        self.log.exception(self.__format(message))

    def critical(self, message):
        self.log.critical(self.__format(message))
