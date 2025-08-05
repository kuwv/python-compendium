# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
# pylint: disable=unused-import
# noqa: F401
"""Control configuration files."""

from __future__ import annotations

import errno
import logging
import os
from collections.abc import Awaitable, MutableMapping
from functools import cached_property
from importlib.util import find_spec
from os import PathLike, path
from types import TracebackType
from typing import Any, Optional, IO, Union

import aiofiles
from aiofiles.threadpool.text import AsyncTextIOWrapper

from compendium.exceptions import ConfigFileError, LoaderError
from compendium.settings import Settings

log = logging.getLogger(__name__)


class ConfigFile:
    """Manage settings loaded from various confiugration file types."""

    __async__ = False
    extensions: tuple[str, ...]

    def __new__(cls, *args: Any, **kwargs: Any) -> ConfigFile:
        """Return state type."""
        if cls is ConfigFile:
            filepath = args[0] if len(args) > 0 else None
            if filepath:
                return cls.init(filepath, *args, **kwargs)
        for loader in list(cls.__subclasses__()):
            if cls.__async__ and loader.__name__.startswith('Async'):
                return super().__new__(loader)
            if (
                not cls.__async__
                and loader.__name__.startswith('Sync')
            ):
                return super().__new__(loader)
        raise LoaderError(
            'no loader could be determined from available loader types'
        )

    # TODO: switch to dependency injection for filetypes
    def __init__(
        self,
        filepath: Union[PathLike, str],
        /,
        filetype: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize single configuration file."""
        self.default_filetype = filetype or kwargs.pop(
            'default_filetype', 'toml'
        )
        self.default_filename = kwargs.pop(
            'default_filename', f"config.{self.default_filetype}"
        )
        if filepath:
            self.filepath = filepath
        else:
            raise TypeError('filepath is undefined')
        self.encoding = kwargs.pop('encoding', 'utf-8')
        self.writable = bool(kwargs.pop('writable', False))
        self.factory: type[MutableMapping] = kwargs.pop('factory', Settings)
        self.factory_kwargs: dict[str, Any] = kwargs.pop('factory_kwargs', {})

    def __eq__(self, other: object) -> bool:
        """Check if path is equal to config file path."""
        if isinstance(other, PathLike) or isinstance(other, str):
            return self.filepath == other
        if isinstance(other, self.__class__):
            return self == other
        return False

    def __repr__(self) -> str:
        """Get filepath."""
        return repr(self.filepath)

    def __str__(self) -> str:
        """Return filepath."""
        return str(self.filepath)

    # @classmethod
    # def create(
    #     cls, config: MutableMapping, filepath: Union[PathLike, str]
    # ) -> ConfigFile:
    #     ...

    @classmethod
    def init(
        cls,
        filepath: Union[PathLike, str],
        /,
        *args: Any,
        **kwargs: Any,
    ) -> ConfigFile:
        if filepath:
            filetype = kwargs.pop('filetype', None)
            if filetype is None:
                filename = path.basename(filepath)
                if filename != '' and '.' in filename:
                    filetype = path.splitext(filename)[-1].strip('.')
            if filetype is None:
                filename = path.basename(filepath)
                if filename != '' and '.' in filename:
                    filetype = path.splitext(filename)[-1].strip('.')
            if filetype is not None:
                for loader in list(cls.__subclasses__()):
                    if filetype in loader.extensions:
                        return loader.__new__(loader, *args, **kwargs)
        raise LoaderError('no loader could be determined from filepath')

    @cached_property
    def filename(self) -> str:
        """Get filename from filepath."""
        return (
            filename
            if (filename := path.basename(self.filepath)) != ''
            else self.default_filename
        )

    @cached_property
    def filetype(self) -> str:
        """Get filetype from filename."""
        if '.' in self.filename:
            return path.splitext(self.filename)[-1].strip('.')
        return self.default_filetype

    # TODO: refactor to overload if possible

    def dump(self, config: MutableMapping) -> Union[Awaitable[None], None]:
        raise NotImplementedError

    def load(self) -> Union[Awaitable[MutableMapping], MutableMapping]:
        raise NotImplementedError


class AsyncConfigFileMixin:
    encoding: str
    factory: type[MutableMapping]
    factory_kwargs: dict[str, Any]
    filepath: Union[PathLike, str]
    writable: bool

    async def __aenter__(self) -> AsyncConfigFileMixin:
        self.settings = await self.load()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self.writable:
            await self.dump(self.settings)

    async def _load(self, file: AsyncTextIOWrapper) -> MutableMapping:
        raise NotImplementedError('_load: missing loader')

    async def _dump(
        self, update: MutableMapping, file: AsyncTextIOWrapper
    ) -> None:
        raise NotImplementedError('_dump: missing loader')

    async def load(self) -> MutableMapping:
        """Load settings from configuration file."""
        if path.exists(self.filepath):
            logging.info('Retrieving configuration: %s', self.filepath)
            # TODO: combine factory and _load
            async with aiofiles.open(
                self.filepath, 'r', encoding=self.encoding
            ) as file:
                config = await self._load(file)
                return self.factory(
                    config, **self.factory_kwargs
                )  # type: ignore
        raise ConfigFileError(
            f"Skipping: no file found at: '{self.filepath}'"
        )

    async def dump(self, config: MutableMapping) -> None:
        """Save settings to configuraiton file."""
        try:
            if self.writable:
                logging.info('Saving configuration: %s', self.filepath)
                # TODO: refactor to use respective dict from chainmap
                async with aiofiles.open(
                    self.filepath, 'w', encoding=self.encoding
                ) as file:
                    await self._dump(config, file)
            else:
                raise ConfigFileError('Error: file is not writable')
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise LoaderError(f"unable to save to '{self.filepath!r}")


class SyncConfigFileMixin:
    encoding: str
    factory: type[MutableMapping]
    factory_kwargs: dict[str, Any]
    filepath: Union[PathLike, str]
    writable: bool

    def __enter__(self) -> SyncConfigFileMixin:
        self.settings = self.load()
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self.writable:
            self.dump(self.settings)

    def _load(self, file: IO) -> MutableMapping:
        raise NotImplementedError('_load: missing loader')

    def _dump(self, update: MutableMapping, file: IO) -> None:
        raise NotImplementedError('_dump: missing loader')

    def load(self) -> MutableMapping:
        """Load settings from configuration file."""
        if path.exists(self.filepath):
            logging.info('Retrieving configuration: %s', self.filepath)
            with open(self.filepath, 'r', encoding=self.encoding) as file:
                config = self._load(file)
                print(config)
                return self.factory(
                    config, **self.factory_kwargs
                )  # type: ignore
        raise ConfigFileError(
            f"Skipping: no file found at: '{self.filepath}'"
        )

    def dump(self, config: MutableMapping) -> None:
        """Save settings to configuraiton file."""
        try:
            if self.writable:
                logging.info('Saving configuration: %s', self.filepath)
                # TODO: refactor to use respective dict from chainmap
                with open(self.filepath, 'w', encoding=self.encoding) as file:
                    self._dump(config, file)
            else:
                raise ConfigFileError('Error: file is not writable')
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise LoaderError(f"unable to save to '{self.filepath!r}")
