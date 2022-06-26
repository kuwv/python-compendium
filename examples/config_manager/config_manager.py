from tempfile import NamedTemporaryFile
from textwrap import dedent

from compendium.config_manager import ConfigManager

# Retrieve settings from config files
cfg = ConfigManager(name='app', filepaths=[file1.name, file2.name])

# Get using dpath
cfg.get('/default/foo2')

# Lookup with multi-query
cfg.lookup('/example/settings/foo', '/default/foo')
