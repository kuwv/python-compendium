# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control YAML configuration module."""

import errno
import logging
import os
# import textwrap
from typing import Any, Dict, Tuple

from ruamel.yaml import YAML  # type: ignore
# from ruamel.yaml.scalarstring import LiteralScalarString

from compendium.filetypes_base import FiletypesBase

# TODO consider strictyaml or poyo
# def literal_scalar_string(content):
#     """Prepare multiline string as yaml scalar."""
#     return LiteralScalarString(textwrap.dedent(content))


class YamlConfig(FiletypesBase):
    """Manage YAML configuration files."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize YAML configuration module."""
        logging.info('Inializing YamlConfig')
        self.encoding = kwargs.get('encoding', 'utf-8')
        self.kind = kwargs.get('kind', None)

    def __yaml_parser(self, kind: str) -> YAML:
        """Get yaml parser."""
        yaml = YAML(typ=kind)
        yaml.explicit_start = True  # type: ignore
        yaml.preserve_quotes = True  # type: ignore
        return yaml

    @staticmethod
    def filetypes() -> Tuple[str, ...]:
        """Return support YAML filetypes."""
        return ('yaml', 'yml')

    def load_config(self, filepath: str) -> Dict[str, Any]:
        """Load settings from YAML configuration."""
        logging.info(
            "loading YAML configuration file {}".format(filepath)
        )
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding=self.encoding) as f:
                yaml = self.__yaml_parser(self.kind or 'safe')
                content = yaml.load(f)
        else:
            content = {}
        return content

    def dump_config(self, content: Dict[str, Any], filepath: str) -> None:
        """Save settings to YAML configuration."""
        try:
            with open(filepath, 'w') as f:
                yaml = self.__yaml_parser(self.kind or 'rt')
                yaml.dump(content, f)
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise
