import os
import compendium
from anymod import PluginLoader  # type: ignore
from compendium.config.config_base import ConfigBase

package_path = os.path.dirname(compendium.__file__)
config_path = os.path.dirname(os.path.realpath(__file__))
toml_path = config_path + '/config.toml'


def test_module_exec():
    '''Dynamically load the appropriate module'''
    compendium_path = compendium.__path__[0].rsplit(os.sep, 1)[0]
    mod = PluginLoader([compendium_path])
    imports = mod.list_imports()
    assert 'compendium.config.filetypes.json' in imports
    assert 'compendium.config.filetypes.toml' in imports
    assert 'compendium.config.filetypes.xml' in imports
    assert 'compendium.config.filetypes.yaml' in imports
    module_path = mod.get_import_path('toml', compendium_path)
    assert module_path == 'compendium.config.filetypes.toml'
    module = mod.retrieve_subclass(module_path, ConfigBase)
    cfg_class = mod.load_classpath(f"{module.__module__}.{module.__name__}")
    cfg = cfg_class()
    settings = cfg.load_config(config_path + '/config.toml')
    assert settings['title'] == 'TOML Example'
