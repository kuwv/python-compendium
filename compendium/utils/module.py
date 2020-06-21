# -*- coding: utf-8 -*-
import importlib
import importlib.machinery
import pkgutil

import pkg_resources

import logging

SUFFIXES = [
    ('Source:', importlib.machinery.SOURCE_SUFFIXES),
    ('Debug:', importlib.machinery.DEBUG_BYTECODE_SUFFIXES),
    ('Optimized:', importlib.machinery.OPTIMIZED_BYTECODE_SUFFIXES),
    ('Bytecode:', importlib.machinery.BYTECODE_SUFFIXES),
    ('Extension:', importlib.machinery.EXTENSION_SUFFIXES),
]


def discover_plugins(self, module_prefix: str = 'lunar_'):
    return {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in pkgutil.iter_modules()
        if name.startswith(module_prefix)
    }


def discover_entry_points(self, entry):
    return {
        entry_point.name: entry_point.load()
        for entry_point
        in pkg_resources.iter_entry_points(entry)
    }


# TODO: should load from pkgutil
# https://packaging.python.org/guides/creating-and-discovering-plugins/
# pluginbase +1
# stevedore -1 only 2.7 and 3.5 ?!?
# importlib +1
class ModuleLoader(object):

    __module_path = None
    __loader = None

    def __init__(self, module_path: str = None):
        if module_path is not None:
            self.__module_path = module_path

    '''
    def find_loader(self, loader_name: str):
        self.__loader = importlib.find_loader(loader_name)

    def load_package_module(self, loader_name: str, module_name: str):
        pkg_loader = self.find_loader(loader_name)
        pkg = pkg_loader.load_module()
        self.__loader = importlib.find_loader(module_name, pkg.__path__)

    def reload_module(self, module_name):
        try:
            module = importlib.reload(module_name)
        except ImportError:
            logging.error("Failed to reload {}".format(module_name))
        return module
    '''

    def load_module(self, module_name: str):
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            logging.error("Failed to load {}".format(module_name))
        return module

    def load_classpath(self, full_class_path: str):
        logging.info("Loading class {}".format(full_class_path))
        try:
            class_data = full_class_path.split('.')
            module_path = '.'.join(class_data[:-1])
            class_name = class_data[-1]
            logging.info(
                "Module: {m} Class: {c}".format(m=module_path, c=class_name)
            )
            module = self.load_module(module_path)
        except ImportError:
            logging.error("Failed to load {}".format(class_name))
        return getattr(module, class_name)
