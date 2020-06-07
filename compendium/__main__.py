from .filetree import FileTree
from .settings import Settings
# from .cli import cli
import os
import json

conpend_home = os.environ.get('COMPEND_HOME')
conpend_conf = os.environ.get('COMPEND_CONF')
conpend_log = os.environ.get('COMPEND_LOG')

filelist = FileTree('test')

controller = Settings(application='tests', filename='settings.toml')


def print_json(var):
    print(json.dumps(var, indent=2, sort_keys=True))


def main():
    print('File paths: ' + str(filelist.filepaths))
    print(filelist.load_config_paths('nested'))
    print_json(var=controller.settings)
    # print_json(controller.get_section('tool'))
    print(controller.list_sections())
