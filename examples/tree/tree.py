import os

# from anytree import RenderTree  # type: ignore

from compendium.config_manager import ConfigManager, TreeConfigManager

data1 = {'key1': 'value1'}
data2 = {'key2': 'value2'}
data3 = {'key3': 'value3'}

n1 = TreeConfigManager('n1', defaults=data1)
assert isinstance(n1, ConfigManager) is True
print('n1', n1)

n2 = TreeConfigManager('n2', defaults=data2, parent=n1)
print('ns', n2)
assert n2.retrieve('/key1') is None
assert n2.retrieve('/key2') == 'value2'

n3 = n2.new_child('n3', data=data3)
print('n3', n3)
print('settings', n3.settings.maps)
assert n3.settings.maps == [{'key3': 'value3'}, {'key2': 'value2'}]
n3.push({'another_key3': 'another_value3'})
assert n3.settings.maps == [
    {'another_key3': 'another_value3'}, {'key3': 'value3'}, {'key2': 'value2'}
]
assert n3.retrieve('/key2') == 'value2'
assert isinstance(n3, ConfigManager) is True
assert n3.retrieve('/key3') == 'value3'

# print(RenderTree(n1))
# for pre, _, node in RenderTree(n1):
#     treestr = u"%s%s" % (pre, node.name)
#     print(treestr.ljust(8), node.data)

tree_dir = os.path.dirname(__file__)
tree_cfg = TreeConfigManager(
    name='test',
    basedir=tree_dir,
    filename='node.toml',
    load_root=True,
    log_level='debug',
)
# tree_cfg.load_configs()
for x in tree_cfg:
    print(x)
