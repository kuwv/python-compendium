# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Example YAML config.'''

import os

from compendium.config_manager import ConfigManager

basepath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(basepath, 'example.yaml')
outpath = os.path.join(basepath, 'example-out.yaml')

cfg = ConfigManager(application='tests')
cfg.load(filepath=filepath)

print('settings', cfg.settings.__dict__)
# print('allowed_roles', cfg.settings.allowed_roles[0])
# print('default_args', cfg.settings.dag.default_args)
# assert 'sre' in cfg.settings.get('/allowed_roles')
# assert 'devops' in cfg.settings.get('/allowed_roles')
# assert 'cloudops' in cfg.settings.get('/allowed_roles')

print('post settings', cfg.settings.data)
cfg.dump(filepath=outpath)

# JSON
jsonin = os.path.join(basepath, 'test.json')
jsonout = os.path.join(basepath, 'out.json')

# YAML
yamlin = os.path.join(basepath, 'test.yaml')
yamlout = os.path.join(basepath, 'out.yaml')

# TOML
tomlin = os.path.join(basepath, 'test.toml')
tomlout = os.path.join(basepath, 'out.toml')

# JSON
jsoncfg = ConfigManager(application='json')
jsoncfg.load(filepath=jsonin)
jsoncfg.dump(filepath=jsonout)
jsoncfg.dump(filepath=yamlout)
jsoncfg.dump(filepath=tomlout)

# YAML
yamlcfg = ConfigManager(application='yaml')
yamlcfg.load(filepath=yamlin)
yamlcfg.dump(filepath=yamlout)
yamlcfg.dump(filepath=jsonout)
jsoncfg.dump(filepath=tomlout)

# TOML
tomlcfg = ConfigManager(application='toml')
tomlcfg.load(filepath=tomlin)
tomlcfg.dump(filepath=tomlout)
tomlcfg.dump(filepath=jsonout)
# tomlcfg.dump(filepath=yamlout)

print('json', type(jsoncfg.settings.data), jsoncfg.settings.data)
for k, v in tomlcfg.settings.data.items():
    print(k, type(v))

print('toml', type(tomlcfg.settings.data), tomlcfg.settings.data)
for k, v in tomlcfg.settings.data.items():
    print(k, type(v))

print('yaml', type(yamlcfg.settings.data), yamlcfg.settings.data)
for k, v in yamlcfg.settings.data.items():
    print(k, type(v))

print('compare', yamlcfg.settings.data == tomlcfg.settings.data)
# tomlcfg.dump(filepath=yamlout)
