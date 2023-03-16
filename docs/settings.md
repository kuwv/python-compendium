# Settings

## Configuration Layers

Layers:

- Default Configurations
- Configuration Files
- Environment Variables

### Defaults

Defaults are settings loaded from a selected configuration file. This configuration is a read only file. Settings provided by defaults are the last settings searched for entries before an error is thrown.

### Configuration Files

Configuration files are the primary storage type for settings. These file can either be user or system configuration files. The last configuration file found is one loaded. This file may optionally read-only or writable.

### Environment Variables

Environment variables are variables provided by the current shell. Variables provided this way are loaded once on startup and are read-only. These settings are the first queried for entries.

```python
>>> from compendium.settings import SettingsProxy

# provide environment variable data to convert
>>> key = 'COMPEND_EXAMPLE_DATA'
>>> value = 12

# represent environment variables
>>> class Environs(SettingsProxy):
...     """Provide environs object."""
...
...     def __init__(self, *args):
...         """Initialize environs."""
...         self.prefix = 'COMPEND'
...         super().__init__(*args)

# initialize environment settings
>>> environs = Environs()
>>> environs.load_dotenv()
>>> _ = environs.load_environs()

# convert environment key to dictionary
>>> environs.to_dict(key, value)
{'compend': {'example': {'data': 12}}}

```

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

```
cfg.get('/servers/**/ip')
```

### Search settings

```
query = cfg.search('/servers/**/ip')
```

## Adding Settings

### Create settings

```
cfg.create('/test', 'test')
```

### Update settings

```
cfg.update('/owner/name', 'Tom Waits')
```

## Remove Settings

### Delete settings

```
cfg.delete('/owner/name')
```
