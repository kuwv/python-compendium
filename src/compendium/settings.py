# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide settings modules."""

import logging
import os
from ast import literal_eval
from collections import ChainMap
from collections.abc import MutableMapping
from string import Template
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    Mapping,
    Optional,
    Tuple,
    Union,
)

import dpath
from dpath.exceptions import PathNotFound

if TYPE_CHECKING:
    from _typeshed import SupportsKeysAndGetItem
    from mypy_extensions import KwArg, VarArg

log = logging.getLogger(__name__)


class Settings(MutableMapping):
    """Manage settings loaded from confiugrations using dpath."""

    separator: str = '/'

    def __init__(self, data: Dict[str, Any], **kwargs: Any) -> None:
        """Initialize settings store."""
        if 'separator' in kwargs:
            Settings.separator = kwargs.pop('separator')
        self.data: Dict[str, Any] = {}
        if data is not None:
            self.update(data)
        if kwargs:
            self.update(kwargs)

    def __delitem__(self, key: str) -> Any:
        """Delete item at key."""
        return dpath.delete(self.data, key, Settings.separator)

    def __iter__(self) -> Iterator[Any]:
        """Iterate settings dictionary."""
        return iter(self.data)

    def __len__(self) -> int:
        """Return number of settings items."""
        return len(self.data)

    def __getitem__(self, key: str) -> Any:
        """Get item."""
        return dpath.get(self.data, key, Settings.separator)

    def __setitem__(self, key: str, value: Any) -> Any:
        """Set item to new value or create it."""
        try:
            self[key]  # pylint: disable=pointless-statement
            dpath.set(self.data, key, value, Settings.separator)
        except KeyError:
            dpath.new(self.data, key, value, Settings.separator)

    def __repr__(self) -> str:
        """Retrun readable representation of settings."""
        template = Template('<$name: $data>')
        return repr(
            template.substitute(name=type(self).__name__, data=self.data)
        )

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get item or return default."""
        try:
            value = self[key]
            return value
        except KeyError:
            return default

    def pop(self, key: str, *default: Any) -> Any:
        """Get item and remove it from settings or return default."""
        try:
            # TODO: need to determine how dpath will handle list element here
            value = self[key]
            del self[key]
            return value
        except (KeyError, PathNotFound):
            return default[0]

    def lookup(
        self,
        *args: str,
        default: Optional[Any] = None,
    ) -> Optional[Any]:
        """Get value from settings from multiple keys."""
        for key in args:
            try:
                value = self[key]
                if value is not None:
                    log.info('lookup found: %s for %s', value, key)
                    return value
            except KeyError:
                log.debug('lookup was unable to query: %s', key)
            log.debug('returning default for: %s', key)
        return default

    def values(self, query: Optional[str] = None) -> Any:
        """Search settings matching query."""
        if query is None:
            template = Template('${separator}*')
            query = template.substitute(separator=Settings.separator)
        return dpath.values(self.data, query, Settings.separator)

    # XXX: not sure if this should stay for dictionary
    def append(self, key: str, value: Any) -> None:
        """Append to a list located at key."""
        store = [value]
        for subkey in reversed(key.split(Settings.separator)):
            if subkey != '':
                store = {subkey: store}  # type: ignore
        dpath.merge(self.data, store)  # type: ignore

    # def update(self, other=(), /, **kwds: Any) -> None:
    def update(
        self,
        other: Union['SupportsKeysAndGetItem', Iterable[Tuple[Any, Any]]] = (),
        /,
        **kwargs: Any,
    ) -> None:
        """Update settings."""
        dpath.merge(
            self.data,
            other or kwargs,  # type: ignore
            flags=2,
        )


class SettingsMap(ChainMap):
    """Manage layered settings loaded from confiugrations using dpath."""

    separator: str = '/'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize settings store."""
        if 'separator' in kwargs:
            SettingsMap.separator = kwargs.pop('separator')
        super().__init__(*args)

    def push(self, data: Dict[str, Any]) -> None:
        """Push settings untop store."""
        logging.debug(data)
        self.maps.insert(0, data)

    # TODO: add capability to recursive search settings

    def __delitem__(self, key: str) -> Any:
        """Delete item at key."""
        return dpath.delete(self.maps[0], key, SettingsMap.separator)

    def __getitem__(self, key: str) -> Any:
        """Get item."""
        for mapping in self.maps:
            try:
                return dpath.get(mapping, key, SettingsMap.separator)
            except KeyError:
                pass
        return self.__missing__(key)

    def __setitem__(self, key: str, value: Any) -> Any:
        """Set item to new value or create it."""
        try:
            self[key]  # pylint: disable=pointless-statement
            dpath.set(self.maps[0], key, value, SettingsMap.separator)
        except KeyError:
            dpath.new(self.maps[0], key, value, SettingsMap.separator)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get item or return default."""
        try:
            value = self[key]
            return value
        except KeyError:
            return default

    def pop(self, key: str, *default: Any) -> Any:
        """Get item and remove it from settings or return default."""
        try:
            # TODO: need to determine how dpath will handle list element here
            value = self[key]
            del self[key]
            return value
        except (KeyError, PathNotFound):
            # self.maps[0].pop(key, *args)
            return default[0]

    def lookup(
        self,
        *args: str,
        default: Optional[Any] = None,
    ) -> Optional[Any]:
        """Get value from settings from multiple keys."""
        for key in args:
            try:
                value = self[key]
                log.info('lookup found: %s for %s', value, key)
                return value
            except KeyError:
                log.debug('lookup was unable to query: %s', key)
            log.debug('returning default for: %s', key)
        return default

    # def values(self, query: Optional[str] = None) -> Dict[str, Any]:
    #     """Search settings matching query."""
    #     if query is None:
    #         query = f"{SettingsMap.separator}*"
    #     return dpath.values(self.maps[0], query, SettingsMap.separator)

    # def append(self, key: str, value: Any) -> None:
    #     """Append to a list located at key."""
    #     store = [value]
    #     for x in reversed(key.split(SettingsMap.separator)):
    #         if x != '':
    #             store = {x: store}  # type: ignore
    #     dpath.merge(self.maps[0], store)

    def update(
        self,
        other: Union['SupportsKeysAndGetItem', Iterable[Tuple[Any, Any]]] = (),
        /,
        **kwargs: Any,
    ) -> None:
        """Update settings."""
        dpath.merge(
            self.maps[0],
            other or kwargs,  # type: ignore
            afilter=None,  # type: ignore
            flags=2,
        )


class SettingsProxy(MutableMapping):
    """Proxy to manage settings with environment variables."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize settings store."""
        self.prefix = kwargs.pop('prefix', 'COMPEND').lower()

        self.__environs = {}
        if kwargs.pop('load_dotenv', False):
            self.load_dotenv()
        if kwargs.pop('load_environs', True):
            self.__environs.update(self.load_environs())

        # super().__init__(*args, **kwargs)
        self.data = SettingsMap(*args, **kwargs)

    @property
    def environs(self) -> Dict[str, Any]:
        """Get environs."""
        return self.__environs

    def __delitem__(self, key: str) -> Any:
        """Delete item at key."""
        del self.data[key]

    def __getattr__(
        self, attr: str
    ) -> 'Callable[[VarArg(Any), KwArg(Any)], Any]':
        """Proxy calls to settings store."""
        if hasattr(self.__dict__.get('data'), attr):

            def wrapper(*args: Any, **kwargs: Any) -> Any:
                """Call query for data store."""
                return getattr(self.data, attr)(*args, **kwargs)

            return wrapper
        raise AttributeError(attr)

    def __getitem__(self, key: str) -> Any:
        """Get environment variable then mapped item."""
        try:
            value = dpath.get(self.environs, key, Settings.separator)
            return value
        except KeyError:
            pass

        value = self.data[key]
        return value

    def __iter__(self) -> Iterator[Any]:
        """Iterate settings dictionary."""
        return self.data.__iter__()

    def __len__(self) -> int:
        """Return number of settings items."""
        return self.data.__len__()

    def __setitem__(self, key: str, value: Any) -> Any:
        """Set item to new value or create it."""
        self.data[key] = value

    def __repr__(self) -> str:
        """Retrun readable representation of settings."""
        return repr(self.data)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get item or return default."""
        try:
            value = self[key]
            return value
        except KeyError:
            return default

    def lookup(
        self,
        *args: str,
        default: Optional[Any] = None,
    ) -> Optional[Any]:
        """Get value from settings from multiple keys."""
        for key in args:
            try:
                value = self[key]
                log.info('lookup found: %s for %s', value, key)
                return value
            except KeyError:
                log.debug('lookup was unable to query: %s', key)
            log.debug('returning default for: %s', key)
        return default

    @classmethod
    def combine(
        cls, source: Dict[str, Any], update: Mapping[str, Any]
    ) -> Dict[str, Any]:
        """Perform recursive merge."""
        for k, v in update.items():
            if isinstance(v, Mapping):
                source[k] = cls.combine(source.get(k, {}), v)
            else:
                source[k] = v
        return source

    @staticmethod
    def to_dict(key: str, value: Any) -> Dict[str, Any]:
        """Convert environment key to nested dictionary."""

        def expand(keypath: str) -> Dict[str, Any]:
            """Convert key part to dictionary key."""
            if '_' not in keypath:
                return {keypath: value}
            k, v = keypath.split('_', 1)
            return {k: expand(v)}

        return expand(key.lower())

    @staticmethod
    def load_dotenv() -> None:
        """Load environs from '.env' file."""
        # TODO: key/value should be added from dotenv regardless of prefix
        env_file = os.path.join(os.getcwd(), '.env')
        if os.path.exists(env_file):
            with open(env_file, encoding='utf-8') as env:
                for line in env:
                    k, v = line.partition('=')[::2]
                    os.environ[k.strip().upper()] = str(v)

    def load_environs(self) -> Dict[str, Any]:
        """Load environment variables."""
        prefix = str(
            f"{self.prefix}_" if self.prefix != '' else self.prefix
        ).upper()
        env: Dict[str, Any] = {}
        for k, v in os.environ.items():
            if k.startswith(prefix):
                env = self.combine(
                    source=env,
                    update=self.to_dict(
                        k.replace(prefix, ''),
                        literal_eval(v) if v.isnumeric() else v,
                    ),
                )
        return env
