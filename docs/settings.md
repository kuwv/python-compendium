# Settings

## Configuration Layers

Layers:

- Environment Variables
- Configuration Files
- Default Configurations

### Environment Variables

Environment variables are variables provided by the current shell. Variables provided this way are loaded once on startup and are read-only. These settings are the first queried for entries.

### Configuration Files

Configuration files are the primary storage type for settings. These file can either be user or system configuration files. The last configuration file found is one loaded. This file may optionally read-only or writable.

### Defaults

Defaults are settings loaded from a selected configuration file. This configuration is a read only file. Settings provided by defaults are the last settings searched for entries before an error is thrown.


## Configuring Settings Manager

`name` - Name of the name instance.

`path` - Path to the configuration files.

`separator` - Character used to separate search paths within search.

`prefix` - Prefix used to pull environment variables from others.

## Managing Settings

```
from compendium.settings import Settings

cfg = Settings(name='app', path='afile.toml')
cfg.load()
```

## Searching Data

### Getting settings

`cfg.get('/servers/**/ip')`

### Search settings

`query = cfg.search('/servers/**/ip')`


## Adding Settings

### Create settings

`cfg.create('/test', 'test')`

### Update settings

`cfg.update('/owner/name', 'Tom Waits')`

## Remove Settings

### Delete settings

`cfg.delete('/owner/name')`
