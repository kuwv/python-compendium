import compendium
import os
import pytest

# from compendium.utils import ModuleLoader
from compendium.config.config_base import ConfigBase

package_path = os.path.dirname(compendium.__file__)
config_path = os.path.dirname(os.path.realpath(__file__))


class ModuleLoader:
    """django.core.files.locks uses low level OS functions, fake it."""
    __module = compendium.utils.ModuleLoader

    def __init__(self, fs):
        """Each fake module expects the fake file system as an __init__
        parameter."""
        # fs represents the fake filesystem; for a real example, it can be
        # saved here and used in the implementation
        pass

    # def list_modules():
    #     return True

    def __getattr__(self, name):
        return getattr(self.__module, name)

@pytest.mark.parametrize('fs', [[None, None,
  {'compendium.utils.ModuleLoader': ModuleLoader}]], indirect=True)
def test_module_exec(fs):
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
