'''Provide example tree usage.'''
import os

from anytree import RenderTree  # type: ignore

from compendium.config_manager import TreeConfigManager

pyproject_cfg = TreeConfigManager(
    name='lockfile_tree',
    filename='pyproject.toml',
    basedir=os.path.join(os.path.dirname(__file__), 'proman'),
    load_root=True,
    load_children=True,
    log_level='debug',
)
# print('namespaces', pyproject_cfg.namespaces)
print(pyproject_cfg)
# pyproject_cfg.load_configs()
# child = pyproject_cfg.new_child('dry')
# print('children', pyproject_cfg.children)
print(RenderTree(pyproject_cfg))

lockfile_cfg = TreeConfigManager(
    name='lockfile_tree',
    filename='proman-lock.json',
    basedir=os.path.join(os.path.dirname(__file__), 'proman'),
    load_root=True,
    load_children=True,
    log_level='debug',
)
print(RenderTree(lockfile_cfg))
