'''Control management of modules dynamically.'''
# -*- coding: utf-8 -*-
import inspect
import importlib
import logging
import pkgutil
import pkg_resources
import sys

from typing import Optional

# Current OS Platform filetypes
FILETYPES = [
    ('Source:', importlib.machinery.SOURCE_SUFFIXES),
    ('Debug:', importlib.machinery.DEBUG_BYTECODE_SUFFIXES),
    ('Optimized:', importlib.machinery.OPTIMIZED_BYTECODE_SUFFIXES),
    ('Bytecode:', importlib.machinery.BYTECODE_SUFFIXES),
    ('Extension:', importlib.machinery.EXTENSION_SUFFIXES),
]


# TODO: should load from pkgutil
# https://packaging.python.org/guides/creating-and-discovering-plugins/
# pluginbase +1
# stevedore -1 only 2.7 and 3.5 ?!?
# importlib +1
class ModuleLoader:
    '''Load modules dynamically.'''

    __module_path = None
    # __loader = None

    def __init__(self, path: Optional[list] = None, prefix: str = ''):
        '''Initialize module search paths.'''
        self.__path = path
        self.__prefix = prefix

    @staticmethod
    def discover_plugins(module_prefix: str):
        '''Retrieve list of modules matching prefix.'''
        return {
            name: importlib.import_module(name)
            for finder, name, ispkg in pkgutil.iter_modules()
            if name.startswith(module_prefix)
        }

    @staticmethod
    def discover_entry_points(entry: str):
        '''Retrieve entry points of module.'''
        return {
            entry_point.name: entry_point.load()
            for entry_point in pkg_resources.iter_entry_points(entry)
        }

    def __mod_path(self, path: str, name: str, **kwargs):
        '''Modify paths.'''
        # TODO: Add exclusions, os.path.relpath
        module = kwargs.get('module', None)
        subclass = kwargs.get('subclass', None)

        module_path = path.replace('/', '.') + '.' + name
        if module and subclass:
            module_path = self.retrieve_subclass(module, subclass)
        return module_path

    def list_modules(self, **kwargs):
        '''Retrieve list of modules from specified path with matching prefix.'''
        result = [
            self.__mod_path(finder.path, name, **kwargs)
            for finder, name, _ in pkgutil.iter_modules(
                path=self.__path, prefix=self.__prefix
            )
        ]
        return result

    def discover_module_path(self, module):
        '''Retrieve module path with matching prefix.'''
        # TODO: add try / catch
        return [x for x in self.list_modules() if (module in x)][0]

    def retrieve_subclass(self, module: str, subclass: object):
        '''Retrieve subclass from module.'''
        module_import = importlib.import_module(module, __name__)
        for attribute_name in dir(module_import):

            attribute = getattr(module_import, attribute_name)

            if inspect.isclass(attribute) and issubclass(attribute, subclass):
                if subclass.__name__ != attribute.__name__:
                    setattr(sys.modules[__name__], module, attribute)
                    return attribute

    def reload_module(self, module_name):
        '''Reload imported module.'''
        try:
            module = importlib.reload(module_name)
        except ImportError:
            logging.error("Failed to reload {}".format(module_name))
        return module

    def load_classpath(self, class_path: str):
        '''Load class from module.'''
        logging.info("Loading class {}".format(class_path))
        try:
            module_path, class_name = class_path.rsplit('.', 1)
            module = importlib.import_module(module_path)
        except ImportError:
            logging.error("Failed to load {}".format(class_name))
        return getattr(module, class_name)
