"""Provide example of ConfigManager."""

import os

from compendium.config_manager import ConfigManager

basepath = os.path.join(os.getcwd(), 'examples', 'config_manager')
config1 = os.path.join(basepath, 'config1.toml')
config2 = os.path.join(basepath, 'config2.toml')

# Retrieve settings from config files
cfg = ConfigManager(filepaths=[config1, config2])

# Get using dpath
assert cfg.get('/default/foo2') == 'bar2'
assert cfg.get('/missing') is None

# Lookup with multi-query
assert cfg.lookup('/example/settings/foo', '/default/foo') == 'baz'
