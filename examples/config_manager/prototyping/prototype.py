# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Example YAML config."""

import logging
import os

# from collections import ChainMap
# from typing import Any, Dict, Mapping, Optional
#
# from dpath import util as dpath
# from dpath.exceptions import PathNotFound

from compendium import ConfigManager, SettingsMap

log = logging.getLogger(__name__)

config1 = {
    'proman': {
        'name': 'app1',
        'version': '1.2.3',
        'description': 'this is an example',
        'defaults': {'enable_feature': False},
    }
}

config2 = {
    'tool': {
        'proman': {
            'enable_feature': True,
            'settings': {
                'files': [{'path': '/some/path/to/file', 'kind': 'yaml'}],
                'writable': True,
            },
        },
        'example': {'version': '1.2.4.dev0'},
    }
}


# NOTE: maybe syould save this if needed later
# class MergeMixin:
#     """Merge dictionaries."""
#
#     @classmethod
#     def merge(
#         self,
#         source: Dict[str, Any],
#         update: Mapping[str, Any]
#     ) -> Dict[str, Any]:
#         """Perform recursive merge."""
#         for k, v in update.items():
#             if isinstance(v, Mapping):
#                 source[k] = self.merge(source.get(k, {}), v)
#             else:
#                 source[k] = v
#         return source


# class SettingsMap(ChainMap, MergeMixin):
#     """Manage layered settings loaded from confiugrations using dpath."""
#
#     separator: str = '/'
#
#     def __init__(self, *args: Any, **kwargs: Any) -> None:
#         """Initialize settings store."""
#         if 'separator' in kwargs:
#             SettingsMap.separator = kwargs.pop('separator')
#         # super(ChainMap, self).__init__(args)
#         super().__init__(*args)
#
#     def push(self, data: Dict[str, Any]) -> None:
#         """Push settings untop store."""
#         logging.debug(data)
#         self.maps.insert(0, data)
#
#     # TODO: add capability to recursive search settings
#
#     def __delitem__(self, keypath: str) -> Any:
#         """Delete item at keypath."""
#         return dpath.delete(self.maps[0], keypath, SettingsMap.separator)
#
#     def __getitem__(self, keypath: str) -> Any:
#         """Get item."""
#         for mapping in self.maps:
#             try:
#                 return dpath.get(mapping, keypath, SettingsMap.separator)
#             except KeyError:
#                 pass
#
#     def __setitem__(self, keypath: str, value: Any) -> Any:
#         """Set item to new value or create it."""
#         try:
#             self.__getitem__(keypath)
#             dpath.set(self.maps[0], keypath, value, SettingsMap.separator)
#         except KeyError:
#             dpath.new(self.maps[0], keypath, value, SettingsMap.separator)
#
#     def get(self, keypath: str, default: Optional[Any] = None) -> Any:
#         """Get item or return default."""
#         try:
#             value = self.__getitem__(keypath)
#             return value
#         except KeyError:
#             return default
#
#     def pop(self, keypath: str, default: Optional[Any] = None) -> Any:
#         """Get item and remove it from settings or return default."""
#         try:
#             # TODO: need to determine how dpath will handle list element here
#             value = self.__getitem__(keypath)
#             self.__delitem__(keypath)
#             return value
#         except (KeyError, PathNotFound):
#             return default
#
#     def lookup(
#         self,
#         *args: str,
#         default: Optional[Any] = None,
#     ) -> Optional[Any]:
#         """Get value from settings from multiple keypaths."""
#         for keypath in args:
#             try:
#                 value = self.__getitem__(keypath)
#                 log.info(f"lookup found: {value} for {keypath}")
#                 return value
#             except KeyError:
#                 log.debug(f"lookup was unable to query: {keypath}")
#         return default
#
#     # def values(self, query: Optional[str] = None) -> Dict[str, Any]:
#     #     """Search settings matching query."""
#     #     if query is None:
#     #         query = f"{SettingsMap.separator}*"
#     #     return dpath.values(self.maps[0], query, SettingsMap.separator)
#
#     # def append(self, keypath: str, value: Any) -> None:
#     #     """Append to a list located at keypath."""
#     #     store = [value]
#     #     for x in reversed(keypath.split(SettingsMap.separator)):
#     #         if x != '':
#     #             store = {x: store}  # type: ignore
#     #     dpath.merge(self.maps[0], store)
#
#     def update(self, data: Dict[str, Any]) -> None:
#         """Update settings."""
#         dpath.merge(self.maps[0], data, afilter=None, flags=2)


if __name__ == '__main__':
    basedir = os.path.dirname(__file__)
    filepaths = [
        os.path.join(basedir, 'config1.toml'),
        os.path.join(basedir, 'config2.toml'),
    ]

    cfg_mgr = ConfigManager(filepaths=filepaths, separator='.')
    assert cfg_mgr.separator == cfg_mgr.data.separator

    version = cfg_mgr.lookup('project.version', 'tool.example.version')
    assert version == '1.2.3'
    assert version != '1.2.4.dev0'

    settings = SettingsMap(config1, config2, separator='.')
    assert settings.separator == '.'
    assert settings['proman'] == settings.lookup('proman')
