"""Provide example tree usage."""
import os

from anytree import RenderTree
from compendium.config_manager import ConfigManager, TreeConfigManager

data1 = {'key1': 'value1'}
data2 = {'key2': 'value2'}
data3 = {'key3': 'value3'}

n1 = TreeConfigManager(name='n1', defaults=data1)
assert isinstance(n1, ConfigManager) is True
print('n1', n1)

n2 = TreeConfigManager(name='n2', defaults=data2, parent=n1)
print('ns', n2)
assert n2.get('/key1') is None
assert n2.get('/key2') == 'value2'

n3 = n2.new_child(data3, name='n3')
print('n3', n3)
print('settings', n3.maps)
# assert n3.settings.maps == [{'key3': 'value3'}, {'key2': 'value2'}]
# n3.push({'another_key3': 'another_value3'})
# assert n3.settings.maps == [
#     {'another_key3': 'another_value3'},
#     {'key3': 'value3'},
#     {'key2': 'value2'},
# ]
assert n3.get('/key2') == 'value2'
assert isinstance(n3, ConfigManager) is True
assert n3.get('/key3') == 'value3'

# print(RenderTree(n1))
# for pre, _, node in RenderTree(n1):
#     treestr = u"%s%s" % (pre, node.name)
#     print(treestr.ljust(8), node.data)

tree_cfg = TreeConfigManager(
    name='fruit',
    basedir=os.path.dirname(__file__),
    filename='node.toml',
    load_root=True,
    load_children=True,
    log_level='debug',
)
# print('namespaces', tree_cfg.namespaces)
print(tree_cfg)
# tree_cfg.load_configs()
# child = tree_cfg.new_child('dry')
# print('children', tree_cfg.children)
print(RenderTree(tree_cfg))

# t = iter(tree_cfg)
# print(next(t))
# print(next(t))
# check = next(t)
# print(check)
# print('parent', check.parent)

# print(RenderTree(t))
