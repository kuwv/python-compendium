# -*- coding: utf-8 -*-
import os
from .utils import Logger


class FileTree(object):

    # TODO: Skip all if already loaded unless 'reload' is passed
    def __init__(self, application, filename="settings.toml"):
        self.__log = Logger(__name__)
        self.filepaths = []
        self.application = application
        self.filename = filename
        self.filetype = filename.split(".")[-1]

        self.load_config_paths()

    def __add_filepath(self, path, file):
        filepath = "{p}/{f}".format(p=path, f=file)
        self.__log.debug("searching for {f}".format(f=filepath))
        if os.path.isfile(filepath):
            self.filepaths.append(filepath)
            self.__log.debug("{f} found".format(f=filepath))
        else:
            self.__log.debug("{f} not found".format(f=filepath))

    @staticmethod
    def __get_supported_filetypes():
        pass

    # TODO: Implement pathlib
    def _retrieve_os_filepaths(self):
        """Load config paths based on priority
        First(lowest) to last(highest)
        1. Load settings.<FILETYPE> from /etc/<APP>
            - /etc/<APP>/settings.<FILETYPE>
            - /etc/<APP>/<CONFIG>.<FILETYPE>
        2. Load user configs
            - ~/.<APP>.<FILETYPE>
            - ~/.<APP>.d/settings.<FILETYPE>
        3. Load config in PWD
            - ./settings.<FILETYPE>
            - ./<CONFIG>.<FILETYPE>
        4. Runtime configs:
            - /etc/sysconfig/<APP>
            - .env
            - <CLI>
        """
        self.__log.info("populating settings locations")
        # TODO: Make directory if not exists

        self.__add_filepath("/etc/" + self.application, self.filename)
        self.__add_filepath(
            "/etc/" + self.application, self.application + "." + self.filetype
        )
        self.__add_filepath(
            os.path.expanduser("~"), "."
            + self.application
            + "."
            + self.filetype
        )
        self.__add_filepath(
            os.path.expanduser("~")
            + "/."
            + self.application
            + ".d",
            self.filename
        )
        self.__add_filepath(os.getcwd(), self.filename)
        self.__add_filepath(
            os.getcwd(),
            self.application + "." + self.filetype
        )

    def _retrieve_nested_filepaths(self):
        self.__add_filepath(
            os.getcwd(),
            self.application + "." + self.filetype
        )

    def load_config_paths(self, pathtype="os"):
        if pathtype == "os":
            self._retrieve_os_filepaths()
        elif pathtype == "nested":
            self._retrieve_nested_filepaths()

    @staticmethod
    def __make_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
