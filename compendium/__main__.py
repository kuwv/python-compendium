from .config_manager import ConfigLayout
from .settings import Settings

# from .cli import cli
import json
import os

# import sys

conpend_home = os.environ.get('COMPEND_HOME')
conpend_conf = os.environ.get('COMPEND_CONF')
conpend_log = os.environ.get('COMPEND_LOG')

content_list = ConfigLayout(application='test', load_strategy='nested')
content_list.load_configs('settings.toml'

# content = Settings(
#     application='tests', filename='settings.toml', load_strategy='nested'
# )
content = Settings(application='tests', path='tests/settings.toml')


def print_json(var):
    print(json.dumps(var, indent=2, sort_keys=True, default=str))


def main():
    # print('filepaths: ' + str(content_list.filepaths))
    # print('File paths: ' + str(content_list.filepaths))
    print_json(var=content.settings)
    # print_json(content.get_section('tool'))
    # print('List sections: ' + str(content.list_sections()))
    # print('List IP\'s: ' + str(content.search('servers.*.ip')))
    # content.update({'test': 'test'})


# if __name__ == '__main__':
#     try:
#         main()
#     except BrokenPipeError as exc:
#         sys.exit(exc.errno)
