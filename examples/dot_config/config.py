'''Provide example for loading dot config file.'''
import os
from compendium.loader import ConfigFile

basepath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(basepath, '.example')


assert os.path.exists(filepath) is True
assert os.path.isfile(filepath) is True


cfg = ConfigFile(filepath=filepath, filetype='yaml')
cfg.load()

print('settings', cfg)
# print('allowed_roles', cfg.allowed_roles[0])
# print('default_args', cfg.dag.default_args)
# assert 'sre' in cfg.get('/allowed_roles')
# assert 'devops' in cfg.get('/allowed_roles')
# assert 'cloudops' in cfg.get('/allowed_roles')
