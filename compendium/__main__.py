from .config_manager import ConfigManager
from .settings import Settings

# from .cli import cli
import os
import json

conpend_home = os.environ.get('COMPEND_HOME')
conpend_conf = os.environ.get('COMPEND_CONF')
conpend_log = os.environ.get('COMPEND_LOG')

config_list = ConfigManager('test')

config = Settings(application='tests', filename='settings.toml')


def print_json(var):
    print(json.dumps(var, indent=2, sort_keys=True))


def main():
    print('File paths: ' + str(config_list.filepaths))
    print(config_list.load_config_paths('nested'))
    print_json(var=config.settings)
    # print_json(config.get_section('tool'))
    print(config.list_sections())
