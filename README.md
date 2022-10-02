# Compendium

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Build Status](https://travis-ci.org/kuwv/python-compendium.svg?branch=master)](https://travis-ci.org/kuwv/python-compendium)
[![codecov](https://codecov.io/gh/kuwv/python-compendium/branch/master/graph/badge.svg)](https://codecov.io/gh/kuwv/python-compendium)

## Overview

Compendium is a layered configuration management tool. It has the capability
to manage configuration files writen in JSON, TOML, XML and YAML. Settings
from these configuration files can then be managed easily with the help of
dpath.

## Documentation

https://kuwv.github.io/python-compendium/

### Install

```
pip install compendium
```

### Manage a configuration file

```python
>>> import os
>>> from compendium import ConfigFile

>>> basedir = os.path.join(os.getcwd(), 'tests')
>>> filepath = os.path.join(basedir, 'config.toml')

>>> cfg = ConfigFile(filepath)
>>> settings = cfg.load()

Simple lookup for title
>>> settings['/title']
'TOML Example'

Query values within list
>>> settings.values('/servers/**/ip')
['10.0.0.1', '10.0.0.2']

Check the current server IP address
>>> settings['/database/server']
'192.168.1.1'

Update the server IP address
>>> settings['/database/server'] = '192.168.1.2'
>>> settings['/database/server']
'192.168.1.2'

Check the database max connections
>>> settings['/database/connection_max']
5000

Delete the max connections
>>> del settings['/database/connection_max']

Check that the max connections have been removed
>>> settings.get('/database/connection_max')

```

### Manage multiple layered configurations

The `ConfigManager` is a layered dictionary mapping. It allows multiple
configurations to be loaded from various files. Settings from each file
is overlapped in order so that the first setting found will be used.

```python
>>> import os

>>> from compendium import ConfigManager

Reference config files from examples
>>> basedir = os.path.join(os.getcwd(), 'examples', 'config_manager')
>>> config1 = os.path.join(basedir, 'config1.toml')
>>> config2 = os.path.join(basedir, 'config2.toml')

Retrieve settings from config files
>>> cfg = ConfigManager(name='app', filepaths=[config1, config2])

Get using dpath
>>> cfg.get('/default/foo2')
'bar2'

Lookup with multi-query
>>> cfg.lookup('/example/settings/foo', '/default/foo')
'baz'

```

### Manage nested configurations

```python
>>> import os

>>> from anytree import RenderTree
>>> from compendium.config_manager import ConfigManager, TreeConfigManager

>>> basedir = os.path.join(os.getcwd(), 'examples', 'tree')

>>> cfg = TreeConfigManager(
...     name='fruit',
...     basedir=basedir,
...     filename='node.toml',
...     load_root=True,
...     load_children=True,
... )

>>> cfg.defaults == {}
True

>>> 'succulant' in cfg['/fruit/children']
True

>>> succulant = cfg.get_config('/fruit/succulant')
>>> succulant.name
'succulant'

```

### Manage configurations using Hierarchy File System (HFS)

TBD
<!--
# ```python
# import os
#
# from compendium.config_manager import HierarchyConfigManager
#
# import pytest
#
# Setup base paths
# >>> base_filepath = os.path.dirname(__file__)
# >>> global_filepath = os.path.expanduser('~')
#
# System paths
# >>> fs.add_real_file(
# ...     source_path=os.path.join(base_filepath, 'settings1.toml'),
# ...     target_path=os.path.join(os.sep, 'etc', 'hierarchy', 'config.toml')
# ... )
#
# User paths
# >>> fs.add_real_file(
# ...     source_path=os.path.join(base_filepath, 'settings2.toml'),
# ...     target_path=os.path.join(global_filepath, '.hierarchy.toml')
# ... )
#
# >>> fs.add_real_file(
# ...     source_path=os.path.join(base_filepath, 'settings3.toml'),
# ...     target_path=os.path.join(
# ...         global_filepath, '.hierarchy.d', 'config.toml'
# ...     )
# ... )
#
# >>> cfg = HierarchyConfigManager(
# ...     name='hierarchy',
# ...     filename='config.toml',
# ...     merge_strategy='overlay',
# ...     enable_system_filepaths=True,
# ...     enable_global_filepaths=True
# ... )
# >>> cfg.load_configs()
#
# ```
-->

### Development

```
poetry shell
poetry install
python -m doctest README.md
```
