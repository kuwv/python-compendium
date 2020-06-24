[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Build Status](https://travis-ci.org/kuwv/python-compendium.svg?branch=master)](https://travis-ci.org/kuwv/python-compendium)
[![codecov](https://codecov.io/gh/kuwv/python-compendium/branch/master/graph/badge.svg)](https://codecov.io/gh/kuwv/python-compendium)

# Compendium

## Overview

Compendium is a simple configuration management tool. It has the capability to manage configuration files writen in JSON, TOML, XML and YAML. Settings from these configuration files can then be managed easily with the help of dpath.

## Install

`pip install compendium`

## Manage configuration

``````
from compendium.settings import Settings

cfg = Settings(application='app', path='afile.toml')
cfg.load()
```

## Search settings

`query = cfg.search('/servers/**/ip')`


## Create settings

`cfg.create('/test', 'test')`

## Update settings

`cfg.update('/owner/name', 'Tom Waits')`

## Delete settings

`cfg.delete('/owner/name')`
