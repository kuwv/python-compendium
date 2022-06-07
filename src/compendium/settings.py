# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide settings modules."""

import logging
import os
from ast import literal_eval
from collections import ChainMap
from collections.abc import MutableMapping
from typing import Any, Dict, Iterator, Mapping, Optional

from dpath import util as dpath
from dpath.exceptions import PathNotFound

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

    def __delitem__(self, keypath: str) -> Any:
        """Delete item at keypath."""
        return dpath.delete(self.data, keypath, Settings.separator)

    def __iter__(self) -> Iterator[Any]:
        """Iterate settings dictionary."""
        return iter(self.data)

    def __len__(self) -> int:
        """Return number of settings items."""
        return len(self.data)

    def __getitem__(self, keypath: str) -> Any:
        """Get item."""
        return dpath.get(self.data, keypath, Settings.separator)

    def __setitem__(self, keypath: str, value: Any) -> Any:
        """Set item to new value or create it."""
        try:
            self.__getitem__(keypath)
            dpath.set(self.data, keypath, value, Settings.separator)
        except KeyError:
            dpath.new(self.data, keypath, value, Settings.separator)

    def __repr__(self) -> str:
        """Retrun readable representation of settings."""
        return f"{type(self).__name__}({repr(self.data)})"

    def get(self, keypath: str, default: Optional[Any] = None) -> Any:
        """Get item or return default."""
        try:
            value = self.__getitem__(keypath)
            return value
        except KeyError:
            return default

    def pop(self, keypath: str, default: Optional[Any] = None) -> Any:
        """Get item and remove it from settings or return default."""
        try:
            # TODO: need to determine how dpath will handle list element here
            value = self.__getitem__(keypath)
            self.__delitem__(keypath)
            return value
        except (KeyError, PathNotFound):
            return default

    def lookup(
        self,
        *args: str,
        default: Optional[Any] = None,
    ) -> Optional[Any]:
        """Get value from settings from multiple keypaths."""
        for keypath in args:
            try:
                value = self.__getitem__(keypath)
                if value is not None:
                    log.info(f"lookup found: {value} for {keypath}")
                    return value
            except KeyError:
                log.debug(f"lookup was unable to query: {keypath}")
        log.debug(f"returning default for: {keypath}")
        return default

    def values(self, query: Optional[str] = None) -> Any:
        """Search settings matching query."""
        if query is None:
            query = f"{Settings.separator}*"
        return dpath.values(self.data, query, Settings.separator)

    # XXX: not sure if this should stay for dictionary
    def append(self, keypath: str, value: Any) -> None:
        """Append to a list located at keypath."""
        store = [value]
        for x in reversed(keypath.split(Settings.separator)):
            if x != '':
                store = {x: store}  # type: ignore
        dpath.merge(self.data, store)

    # def update(self, other=(), /, **kwds: Any) -> None:
    def update(  # type: ignore
        self, other: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Update settings."""
        dpath.merge(self.data, other, afilter=None, flags=2)


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

    def __delitem__(self, keypath: str) -> Any:
        """Delete item at keypath."""
        return dpath.delete(self.maps[0], keypath, SettingsMap.separator)

    def __getitem__(self, keypath: str) -> Any:
        """Get item."""
        for mapping in self.maps:
            try:
                return dpath.get(mapping, keypath, SettingsMap.separator)
            except KeyError:
                pass
        return self.__missing__(keypath)

    def __setitem__(self, keypath: str, value: Any) -> Any:
        """Set item to new value or create it."""
        try:
            self.__getitem__(keypath)
            dpath.set(self.maps[0], keypath, value, SettingsMap.separator)
        except KeyError:
            dpath.new(self.maps[0], keypath, value, SettingsMap.separator)

    def get(self, keypath: str, default: Optional[Any] = None) -> Any:
        """Get item or return default."""
        try:
            value = self.__getitem__(keypath)
            return value
        except KeyError:
            return default

    def pop(self, keypath: str, default: Optional[Any] = None) -> Any:
        """Get item and remove it from settings or return default."""
        try:
            # TODO: need to determine how dpath will handle list element here
            value = self.__getitem__(keypath)
            self.__delitem__(keypath)
            return value
        except (KeyError, PathNotFound):
            return default

    def lookup(
        self,
        *args: str,
        default: Optional[Any] = None,
    ) -> Optional[Any]:
        """Get value from settings from multiple keypaths."""
        for keypath in args:
            try:
                value = self.__getitem__(keypath)
                log.info(f"lookup found: {value} for {keypath}")
                return value
            except KeyError:
                log.debug(f"lookup was unable to query: {keypath}")
        log.debug(f"returning default for: {keypath}")
        return default

    # def values(self, query: Optional[str] = None) -> Dict[str, Any]:
    #     """Search settings matching query."""
    #     if query is None:
    #         query = f"{SettingsMap.separator}*"
    #     return dpath.values(self.maps[0], query, SettingsMap.separator)

    # def append(self, keypath: str, value: Any) -> None:
    #     """Append to a list located at keypath."""
    #     store = [value]
    #     for x in reversed(keypath.split(SettingsMap.separator)):
    #         if x != '':
    #             store = {x: store}  # type: ignore
    #     dpath.merge(self.maps[0], store)

    def update(  # type: ignore
        self, other: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Update settings."""
        dpath.merge(self.maps[0], other, afilter=None, flags=2)


class EnvironSettings:
    """Manage environment settings with proxy to other settings."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize settings store."""
        self.prefix = kwargs.pop('prefix', 'COMPEND').lower()

        self.environs = {}
        if kwargs.pop('load_dotenv', False):
            self.load_dotenv()
        if kwargs.pop('load_environs', True):
            self.environs.update(self.load_environs())

        # super().__init__(*args, **kwargs)
        self.data = SettingsMap(*args, **kwargs)

    def __delitem__(self, keypath: str) -> Any:
        """Delete item at keypath."""
        self.data.__delitem__(keypath)

    def __getitem__(self, keypath: str) -> Any:
        """Get environment variable then mapped item."""
        try:
            value = dpath.get(self.environs, keypath, Settings.separator)
            return value
        except KeyError:
            pass

        value = self.data.__getitem__(keypath)
        return value

    def __iter__(self) -> Iterator[Any]:
        """Iterate settings dictionary."""
        return self.data.__iter__()

    def __len__(self) -> int:
        """Return number of settings items."""
        return self.data.__len__()

    def __setitem__(self, keypath: str, value: Any) -> Any:
        """Set item to new value or create it."""
        self.data.__setitem__(keypath, value)

    def __repr__(self) -> str:
        """Retrun readable representation of settings."""
        return self.data.__repr__()

    def get(self, keypath: str, default: Optional[Any] = None) -> Any:
        """Get item or return default."""
        try:
            value = self.__getitem__(keypath)
            return value
        except KeyError:
            return default

    def lookup(
        self,
        *args: str,
        default: Optional[Any] = None,
    ) -> Optional[Any]:
        """Get value from settings from multiple keypaths."""
        for keypath in args:
            try:
                value = self.__getitem__(keypath)
                log.info(f"lookup found: {value} for {keypath}")
                return value
            except KeyError:
                log.debug(f"lookup was unable to query: {keypath}")
        log.debug(f"returning default for: {keypath}")
        return default

    @classmethod
    def combine(
        cls,
        source: Dict[str, Any],
        update: Mapping[str, Any]
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
        """Convert environment keypath to nested dictionary."""
        def expand(x: str) -> Dict[str, Any]:
            """Convert key part to dictionary key."""
            if '_' not in x:
                return {x: value}
            k, v = x.split('_', 1)
            return {k: expand(v)}
        return expand(key.lower())

    @staticmethod
    def load_dotenv() -> None:
        """Load environs from .env file."""
        # TODO: key/value should be added from dotenv regardless of prefix
        env_file = os.path.join(os.getcwd(), '.env')
        if os.path.exists(env_file):
            with open(env_file) as env:
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
                        literal_eval(v) if v.isnumeric() else v
                    )
                )
        return env
