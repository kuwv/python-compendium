# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide query capabilities."""

from typing import Any, Dict, Optional

from dpath import util as dpath  # type: ignore


class DpathMixin:
    """Provide XPath like query capability."""

    separator: str = '/'

    def retrieve(
        self,
        query,
        default: Any = None,
        document: Optional['DpathMixin'] = None,
    ) -> Optional[Any]:
        """Get value from settings with key."""
        if not document:
            document = self
        try:
            return dpath.get(document, query, DpathMixin.separator)
        except KeyError:
            return default

    def search(self, query: str) -> Dict[str, Any]:
        """Search settings matching query."""
        return dpath.values(self, query, DpathMixin.separator)

    def append(self, keypath: str, value: Any) -> None:
        """Append to a list located at keypath."""
        store = [value]
        keypath_dir = keypath.split(DpathMixin.separator)[1:]
        for x in reversed(keypath_dir):
            store = {x: store}  # type: ignore
        dpath.merge(self, store)

    def set(self, keypath: str, value: Any) -> None:
        """Update value located at keypath."""
        dpath.set(self, keypath, value, DpathMixin.separator)

    def add(self, keypath: str, value: Any) -> None:
        """Add key/value pair located at keypath."""
        dpath.new(self, keypath, value, DpathMixin.separator)

    def create(self, keypath: str, value: Any) -> None:
        """Create new key/value pair located at path."""
        dpath.new(self, keypath, value, DpathMixin.separator)

    def delete(self, keypath: str) -> None:
        """Delete key/value located at keypath."""
        dpath.delete(self, keypath, DpathMixin.separator)

    def combine(self, document: Optional[Dict[str, Any]] = None) -> None:
        """Combine document."""
        dpath.merge(self, document, flags=2)
