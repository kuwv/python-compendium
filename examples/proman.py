"""Provide example tree usage."""
import os

from anytree import RenderTree

from compendium.config_manager import TreeConfigManager

pyproject_cfg = TreeConfigManager(
    name='source_tree',
    filename='pyproject.toml',
    basedir=os.path.join(os.path.dirname(__file__), 'proman'),
    load_root=True,
    load_children=True,
    log_level='debug',
)
# print('namespaces', pyproject_cfg.namespaces)
# print('root', pyproject_cfg)
# pyproject_cfg.load_configs()
# print('children', pyproject_cfg.children)
print(RenderTree(pyproject_cfg))

# lockfile_cfg = TreeConfigManager(
#     name='lockfile',
#     filename='proman-lock.json',
#     basedir=os.path.join(os.path.dirname(__file__), 'proman'),
#     load_root=True,
#     load_children=True,
#     log_level='debug',
# )
# print(RenderTree(lockfile_cfg))
