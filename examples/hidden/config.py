# type: ignore
"""Provide example for loading dot config file."""

import os
from compendium.loader import ConfigFile

# from compendium.filetypes.ini import IniConfig
# from pprint import pprint

basepath = os.path.dirname(__file__)
filepath = os.path.join(basepath, '.example')

assert os.path.exists(filepath) is True
assert os.path.isfile(filepath) is True

cfg = ConfigFile(filepath=filepath, default_filetype='yaml')
settings = cfg.load()
print('settings', settings)

assert 'sre' in settings.get('/allowed_roles')
assert 'devops' in settings.get('/allowed_roles')
assert 'cloudops' in settings.get('/allowed_roles')

pypirc_filepath = os.path.join(os.path.expanduser('~'), '.pypirc')

assert os.path.exists(pypirc_filepath) is True, 'a ".pypirc" path should exist'
assert os.path.isfile(pypirc_filepath) is True, 'path should be a file'

pypirc = ConfigFile(pypirc_filepath, default_filetype='ini')
pypirc.load()
print('pypi', type(pypirc))

# pypirc = IniConfig()
# p = pypirc.load_config(pypirc_filepath)
# pprint(p)
