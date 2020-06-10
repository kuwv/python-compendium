# from .config_manager import ConfigManager
from .settings import Settings

# from .cli import cli
import os
import json

conpend_home = os.environ.get('COMPEND_HOME')
conpend_conf = os.environ.get('COMPEND_CONF')
conpend_log = os.environ.get('COMPEND_LOG')

# content_list = ConfigManager('test')
# content = Settings(
#     application='tests', filename='settings.toml', load_strategy='nested'
# )

content = Settings(application='tests', path='tests/settings.toml')


def print_json(var):
    print(json.dumps(var, indent=2, sort_keys=True))


def main():
    # print('File paths: ' + str(content_list.filepaths))
    # print(content_list.load('nested'))
    print_json(var=content.settings)
    # print_json(content.get_section('tool'))
    print(content.list_sections())
