# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide settings modules."""

import logging
import os
from collections import ChainMap
from typing import Any, Dict, Mapping

from compendium.query import DpathMixin


class MergeMixin:
    """Merge dictionaries."""

    @classmethod
    def merge(
        self,
        source: Dict[str, Any],
        update: Mapping[str, Any]
    ) -> Dict[str, Any]:
        """Perform recursive merge."""
        for k, v in update.items():
            if isinstance(v, Mapping):
                source[k] = self.merge(source.get(k, {}), v)
            else:
                source[k] = v
        return source


class EnvironsMixin(MergeMixin):
    """Manage environment variables."""

    @property
    def prefix(self) -> str:
        """Get environment prefix."""
        if hasattr(self, '_prefix'):
            return self._prefix.upper()
        else:
            return 'COMPEND'

    @prefix.setter
    def prefix(self, prefix: str) -> None:
        """Set environment prefix."""
        self._prefix = prefix

    @staticmethod
    def to_dict(key: str, value: Any) -> Dict[str, Any]:
        """Convert environment key to dictionary."""

        def expand(x):
            """Convert key part to dictionary key."""
            if '_' not in x:
                return {x: value}
            k, v = x.split('_', 1)
            return {k: expand(v)}

        return expand(key.lower())

    @staticmethod
    def load_dotenv() -> None:
        """Load environs from .env file."""
        env_file = os.path.join(os.getcwd(), '.env')
        # if self._check_filepath(env_file):
        if os.path.exists(env_file):
            with open(env_file) as env:
                for line in env:
                    k, v = line.partition('=')[::2]
                    os.environ[k.strip().upper()] = str(v)

    def load_environs(self, force: bool = False) -> Dict[str, Any]:
        """Load environment variables."""
        prefix = str(f"{self.prefix}_" if self.prefix != '' else self.prefix)
        env: Dict[str, Any] = {}
        for k, v in os.environ.items():
            if k.startswith(prefix):
                env = self.merge(env, self.to_dict(k.replace(prefix, ''), v),)
        return env


class SettingsMap(ChainMap, DpathMixin, MergeMixin):
    """Manage settings loaded from confiugrations using dpath."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize settings store."""
        super().__init__(*args)
        if 'separator' in kwargs:
            DpathMixin.separator = kwargs.pop('separator')

    def push(self, settings: Dict[str, Any]) -> None:
        """Push settings untop store."""
        logging.debug(settings)
        self.maps.insert(0, settings)

    # TODO: add capability to recursive search settings
