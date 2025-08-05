from importlib.util import find_spec
from os import PathLike
from typing import Any, Awaitable, MutableMapping, Protocol, Union

from compendium.loader.base import ConfigFile
from compendium.loader.ini import IniConfig
from compendium.loader.json import JsonConfig

if find_spec('tomlkit'):
    from compendium.loader.toml import TomlConfig

if find_spec('ruamel.yaml'):
    from compendium.loader.yaml import YamlConfig

if find_spec('xmltodict'):
    from compendium.loader.xml import XmlConfig


class Config(Protocol):
    filepath: Union[PathLike, str]
    encoding: str
    writable: bool
    factory: type[MutableMapping]
    factory_kwargs: dict[str, Any]

    def load(self) -> Union[Awaitable[MutableMapping], MutableMapping]:
        """Load settings from configuration file."""

    def dump(self, config: MutableMapping) -> Union[Awaitable[None], None]:
        """Save settings to configuraiton file."""
