# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control YAML configuration module."""

from __future__ import annotations

import logging
from collections.abc import MutableMapping
from io import StringIO
from os import PathLike, path
from typing import Any, IO, Union

from aiofiles.threadpool.text import AsyncTextIOWrapper
from ruamel.yaml import YAML

# from ruamel.yaml.scalarstring import LiteralScalarString

from compendium import config
from compendium.loader.base import (
    AsyncConfigFileMixin, ConfigFile, SyncConfigFileMixin
)
from compendium.exceptions import LoaderError

# TODO consider strictyaml or poyo
# def literal_scalar_string(content):
#     """Prepare multiline string as yaml scalar."""
#     return LiteralScalarString(textwrap.dedent(content))


class YamlConfig(ConfigFile):
    """Manage YAML configuration files."""

    extensions = ('yaml', 'yml')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize YAML configuration module."""
        logging.info('Inializing YamlConfig')
        self.kind = kwargs.pop('kind', None)
        super().__init__(*args, **kwargs)

    @classmethod
    def yaml_parser(cls, kind: str) -> YAML:
        """Get yaml parser."""
        yaml = YAML(typ=kind)
        yaml.explicit_start = True
        yaml.preserve_quotes = True
        return yaml


class AsyncYamlConfig(AsyncConfigFileMixin, YamlConfig):
    """Manage YAML configurations."""

    async def _load(self, file: AsyncTextIOWrapper) -> MutableMapping:
        """Load settings from YAML configuration."""
        logging.info('loading YAML configuration file')
        parser = self.yaml_parser(self.kind or 'safe')
        content = await file.read()
        return parser.load(content)

    async def _dump(
        self, content: MutableMapping, file: AsyncTextIOWrapper
    ) -> None:
        """Save settings to YAML configuration."""
        logging.info('saving YAML configuration file')
        stream = StringIO()
        parser = self.yaml_parser(self.kind or 'rt')
        parser.dump(content, stream)
        await file.write(stream.getvalue())


class SyncYamlConfig(SyncConfigFileMixin, YamlConfig):
    """Manage YAML configuration files."""

    def _load(self, file: IO) -> MutableMapping:
        """Load settings from YAML configuration."""
        logging.info('loading YAML configuration file')
        yaml = self.yaml_parser(self.kind or 'safe')
        return yaml.load(file.read())

    def _dump(
        self, content: MutableMapping, file: IO
    ) -> None:
        """Save settings to YAML configuration."""
        stream = StringIO()
        yaml = self.yaml_parser(self.kind or 'rt')
        yaml.dump(dict(content), stream)
        file.write(stream.getvalue())
