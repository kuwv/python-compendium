# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control YAML configuration module."""

from __future__ import annotations

import errno
import logging
from io import StringIO
from os import path
from typing import Any

import aiofiles
from ruamel.yaml import YAML

# from ruamel.yaml.scalarstring import LiteralScalarString

from compendium import config
from compendium.exceptions import LoaderError
from compendium.filetypes import FiletypesBase

# TODO consider strictyaml or poyo
# def literal_scalar_string(content):
#     """Prepare multiline string as yaml scalar."""
#     return LiteralScalarString(textwrap.dedent(content))


class YamlConfig(FiletypesBase):
    """Manage YAML configuration files."""

    extensions = ('yaml', 'yml')

    def __new__(cls, *_: Any, **kwargs: Any) -> YamlConfig:
        """Return state type."""
        return super().__new__(
            AsyncYamlConfig
            if kwargs.get('async', config.DEFAULT_ASYNC_ENABLED)
            else SyncYamlConfig
        )

    def __init__(self, **kwargs: Any) -> None:
        """Initialize YAML configuration module."""
        logging.info('Inializing YamlConfig')
        self.encoding = kwargs.get('encoding', 'utf-8')
        self.kind = kwargs.get('kind', None)

    @classmethod
    def yaml_parser(cls, kind: str) -> YAML:
        """Get yaml parser."""
        yaml = YAML(typ=kind)
        yaml.explicit_start = True
        yaml.preserve_quotes = True
        return yaml


class SyncYamlConfig(YamlConfig):
    """Manage YAML configuration files."""

    def load_config(self, filepath: str) -> dict[str, Any]:
        """Load settings from YAML configuration."""
        logging.info('loading YAML configuration file %s', filepath)
        if path.exists(filepath):
            if path.isfile(filepath):
                with open(filepath, 'r', encoding=self.encoding) as file:
                    yaml = self.yaml_parser(self.kind or 'safe')
                    return yaml.load(file.read())
            raise LoaderError(f"filepath '{filepath!r}' is not a file")
        raise LoaderError(f"filepath '{filepath}' does not exist")

    def dump_config(self, content: dict[str, Any], filepath: str) -> None:
        """Save settings to YAML configuration."""
        try:
            with open(filepath, 'w', encoding=self.encoding) as file:
                stream = StringIO()
                yaml = self.yaml_parser(self.kind or 'rt')
                yaml.dump(content, stream)
                file.write(stream.getvalue())
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise LoaderError(f"unable to save to '{filepath!r}")


class AsyncYamlConfig(YamlConfig):
    """Manage toml configurations."""

    async def load_config(self, filepath: str) -> dict[str, Any]:
        """Load settings from toml configuration."""
        logging.info('loading TOML configuration file')
        if path.exists(filepath):
            if path.isfile(filepath):
                async with aiofiles.open(
                    filepath, 'r', encoding=self.encoding
                ) as file:
                    parser = self.yaml_parser(self.kind or 'safe')
                    content = await file.read()
                    return parser.load(content)
            raise LoaderError(f"filepath '{filepath!r}' is not a file")
        raise LoaderError(f"filepath '{filepath!r}' does not exist")

    async def dump_config(
        self, content: dict[str, Any], filepath: str
    ) -> None:
        """Save settings to toml configuration."""
        logging.info('saving TOML configuration file')
        try:
            async with aiofiles.open(
                filepath, 'w', encoding=self.encoding
            ) as file:
                stream = StringIO()
                parser = self.yaml_parser(self.kind or 'rt')
                parser.dump(content, stream)
                await file.write(stream.getvalue())
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise LoaderError(f"unable to save to '{filepath!r}")
