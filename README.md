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

Example `afile.toml`:
```
[default]
foo = "bar"
```

Example `bfile.toml`:
```
[example.settings]
foo = "baz"
```

```
from compendium.config_manager import ConfigManager

cfg = ConfigManager(name='app', filepaths=['afile.toml', 'bfile.toml'])

result = cfg.lookup('/default/foo', '/example/settings/foo')
assert result == 'baz'
```

### Search settings

```
result = cfg.search('/servers/**/ip')
```

### Create settings

```
cfg.create('/test', 'test')
```

### Update settings

```
cfg.set('/owner/name', 'Tom Waits')
```

### Delete settings

```
cfg.delete('/owner/name')
```
