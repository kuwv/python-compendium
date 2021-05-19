'''Provide example for loading dot config file.'''
import os
from compendium.loader import ConfigFile
from compendium.filetypes.ini import IniConfig

# basepath = os.path.dirname(os.path.realpath(__file__))
# filepath = os.path.join(basepath, '.example')
#
# assert os.path.exists(filepath) is True
# assert os.path.isfile(filepath) is True
#
# cfg = ConfigFile(filepath=filepath, filetype='yaml')
# cfg.load()
# print('settings', cfg)
#
# assert 'sre' in cfg.retrieve('/allowed_roles')
# assert 'devops' in cfg.retrieve('/allowed_roles')
# assert 'cloudops' in cfg.retrieve('/allowed_roles')

pypirc_filepath = os.path.join(os.path.expanduser('~'), '.pypirc')

assert os.path.exists(pypirc_filepath) is True
assert os.path.isfile(pypirc_filepath) is True

# pypirc = ConfigFile(pypirc_filepath, filetype='ini')
# pypirc.load()
# print('pypi', type(pypirc))

pypirc = IniConfig()
p = pypirc.load_config(pypirc_filepath)
print(p)
