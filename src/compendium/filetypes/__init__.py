# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide plugin base for configuration modules."""

from abc import ABCMeta, abstractmethod
from typing import Any, Awaitable, Union


class FiletypesBase(metaclass=ABCMeta):
    """Define required configuration module methods."""

    extensions: tuple[str, ...]

    @abstractmethod
    def load_config(self, filepath: str) -> Union[Awaitable, dict[str, Any]]:
        """Load configuration from file."""

    @abstractmethod
    def dump_config(
        self, content: dict[str, Any], filepath: str
    ) -> Union[Awaitable, None]:
        """Save confgration to file."""
