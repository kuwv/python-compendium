```python
>>> from compendium.settings import Settings

>>> settings = Settings(
...     {
...         'compend': {
...              'example': {
...                  'data': 12
...              }
...         },
...         'servers': [
...             {
...                 'name': 'alpha',
...                 'ip': '10.0.0.1',
...                 'dc': 'eqdc10'
...             },
...             {
...                 'name': 'beta',
...                 'ip': '10.0.0.2',
...                 'dc': 'eqdc10'
...             }
...         ]
...     }
... )

# example `__getitem__`
>>> settings['/compend/example/data']
12

# example `get()` with non-existant key
>>> settings.get('/nada/does/not/exist', 'yey')
'yey'

# example `pop()`
>>> settings.pop('/compend')
{'example': {'data': 12}}

# example `pop()` for non-existant key
>>> settings.pop('/nada/does/not/exist', 'yey')
'yey'

# example `values()`
>>> settings.values()
[[{'name': 'alpha', 'ip': '10.0.0.1', 'dc': 'eqdc10'}, {'name': 'beta', 'ip': '10.0.0.2', 'dc': 'eqdc10'}]]

# example `values()` path
>>> settings.values('/servers/**/ip')
['10.0.0.1', '10.0.0.2']

# example `__setitem__()`
>>> settings['/foo'] = 'bar'
>>> settings['/foo']
'bar'

# example `__contains__()`
>>> 'foo' in settings
True

# example `update()`
>>> settings.update({'servers': {'location': 'Virginia'}})
>>> settings['/servers/location']
'Virginia'

# example `del`
>>> del settings['/servers/location']
>>> settings.get('/servers/location')

# example `clear()`
>>> settings.clear()
>>> settings.items()
ItemsView('<Settings: {}>')

```
