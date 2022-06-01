# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide query capabilities."""

import logging
from typing import Any, Dict, Optional

from dpath import util as dpath

log = logging.getLogger(__name__)


# TODO: test anytree as replacement
class DpathMixin:
    """Provide XPath like query capability."""

    separator: str = '/'

    def lookup(
        self,
        *args: str,
        default: Any = None,
        document: Optional['DpathMixin'] = None,
    ) -> Optional[Any]:
        """Get value from settings from multiple keypaths."""
        if not document:
            document = self
        for query in args:
            try:
                result = dpath.get(document, query, DpathMixin.separator)
                if result is not None:
                    log.info(f"lookup found: {result} for {query}")
                    return result
            except KeyError:
                log.debug(f"lookup was unable to query: {query}")
        return default

    def retrieve(
        self,
        query: str,
        default: Any = None,
        document: Optional['DpathMixin'] = None,
    ) -> Optional[Any]:
        """Get value from settings with key."""
        if not document:
            document = self
        try:
            result = dpath.get(document, query, DpathMixin.separator)
            log.info(f"retrieve found: {result} for {query}")
            return result
        except KeyError:
            log.debug(
                f"retrieve was unable to query {query} using default{default}"
            )
            return default

    def search(self, query: str) -> Dict[str, Any]:
        """Search settings matching query."""
        return dpath.values(self, query, DpathMixin.separator)

    def append(self, keypath: str, value: Any) -> None:
        """Append to a list located at keypath."""
        store = [value]
        for x in reversed(keypath.split(DpathMixin.separator)):
            if x != '':
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
