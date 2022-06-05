# Compendium

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Build Status](https://travis-ci.org/kuwv/python-compendium.svg?branch=master)](https://travis-ci.org/kuwv/python-compendium)
[![codecov](https://codecov.io/gh/kuwv/python-compendium/branch/master/graph/badge.svg)](https://codecov.io/gh/kuwv/python-compendium)

## Overview

Compendium is a simple configuration management tool. It has the capability to manage configuration files writen in JSON, TOML, XML and YAML. Settings from these configuration files can then be managed easily with the help of dpath.

## Documentation

https://kuwv.github.io/python-compendium/

### Install

`pip install compendium`

### Manage multiple configurations

```python
>>> from tempfile import NamedTemporaryFile
>>> from textwrap import dedent

>>> from compendium.config_manager import ConfigManager

>>> try:
...     file1 = NamedTemporaryFile(mode='wt', suffix='.toml')
...     _ = file1.write(
...         dedent(
...             """\
...             [default]
...             foo = "bar"
...             foo2 = "bar2"
...             """
...         )
...     )
...     _ = file1.seek(0)
...
...     file2 = NamedTemporaryFile(mode='wt', suffix='.toml')
...     _ = file2.write(
...         dedent(
...             """\
...             [example.settings]
...             foo = "baz"
...             """
...         )
...     )
...     _ = file2.seek(0)
...
...     cfg = ConfigManager(name='app', filepaths=[file1.name, file2.name])
...     cfg.lookup('/example/settings/foo', '/default/foo')
...     cfg.lookup('/default/foo2')
... finally:
...     file1.close()
...     file2.close()
'baz'
'bar2'

```

### Search settings

```python
result = cfg.search('/servers/**/ip')
```

### Create settings

```python
cfg.create('/test', 'test')
```

### Update settings

```python
cfg.set('/owner/name', 'Tom Waits')
```

### Delete settings

```python
cfg.delete('/owner/name')
```
