[![Build Status](https://travis-ci.org/kuwv/python-compendium.svg?branch=master)](https://travis-ci.org/kuwv/python-compendium)
[![codecov](https://codecov.io/gh/kuwv/python-compendium/branch/master/graph/badge.svg)](https://codecov.io/gh/kuwv/python-compendium)

# Compendium

## Overview

Compendium is a simple configuration management tool. It has the capability to manage configuration files writen in JSON, TOML, XML and YAML. Settings from these configuration files can then be managed easily with the help of dpath.

## Install

`pip install compendium`

## Search settings

```
from compendium.settings import Settings

cfg = Settings(application='app', path='afile.toml')
cfg.load()
query = cfg.search('/servers/**/ip')
```


## Create settings

```
from compendium.settings import Settings

cfg = Settings(application='app', path='afile.toml')
cfg.load()
cfg.create('/test', 'test')
```

## Update settings

```
from compendium.settings import Settings

cfg = Settings(application='app', path='afile.toml', writable=True)
cfg.load()
cfg.update('/owner/name', 'Tom Waits')
```

## Delete settings

```
from compendium.settings import Settings

cfg = Settings(application='app', path='afile.toml')
cfg.load()
cfg.delete('/owner/name')
```
