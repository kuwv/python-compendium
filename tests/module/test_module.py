import os
import compendium
from anymod import ModuleLoader
from compendium.config.config_base import ConfigBase

package_path = os.path.dirname(compendium.__file__)
config_path = os.path.dirname(os.path.realpath(__file__))
toml_path = config_path + '/settings.toml'


def test_module_exec():
    '''Dynamically load the appropriate module'''
    mod = ModuleLoader(['compendium/config/filetypes'])
    assert mod.list_modules() == [
        'compendium.config.filetypes.json',
        'compendium.config.filetypes.toml',
        'compendium.config.filetypes.xml',
        'compendium.config.filetypes.yaml'
    ]
    module_path = mod.discover_module_path('toml')
    assert module_path == 'compendium.config.filetypes.toml'
    module = mod.retrieve_subclass(module_path, ConfigBase)
    cfg_class = mod.load_classpath(module.__module__ + '.' + module.__name__)
    cfg = cfg_class()
    settings = cfg.load_config(config_path + '/settings.toml')
    assert settings['title'] == 'TOML Example'
