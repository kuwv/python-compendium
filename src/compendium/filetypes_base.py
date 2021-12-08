# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide plugin base for configuration modules."""

from abc import ABCMeta, abstractmethod
from typing import Any, Dict


class FiletypesBase(metaclass=ABCMeta):
    """Define required configuration module methods."""

    # @abstractproperty
    # def filesystems():
    #     """Retrieve filetypes of filetypes."""

    @abstractmethod
    def load_config(self, filepath: str) -> Dict[str, Any]:
        """Load configuration from file."""

    @abstractmethod
    def dump_config(self, content: Dict[str, Any], filepath: str) -> None:
        """Save confgration to file."""
