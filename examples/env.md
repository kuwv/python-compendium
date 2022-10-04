```python
>>> from collections import UserDict

>>> from compendium.settings import SettingsProxy

>>> key = 'COMPEND_EXAMPLE_DATA'
>>> value = 12


>>> class Environs(UserDict, SettingsProxy):
...     """Provide environs object."""
...
...     def __init__(self, *args):
...         """Initialize environs."""
...         self.prefix = 'COMPEND'
...         super().__init__(*args)
...
...     def __repr__(self):
...         """Provide string representation of environs."""
...         return repr(Environs)


>>> environs = Environs()
>>> environs.load_dotenv()
>>> _ = environs.load_environs()
>>> environs.to_dict(key, value)
{'compend': {'example': {'data': 12}}}

```
