# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control YAML configuration module."""

import errno
import logging
import os

# import textwrap
from typing import Any, Dict, Tuple

from ruamel.yaml import YAML

# from ruamel.yaml.scalarstring import LiteralScalarString

from compendium.filetypes import FiletypesBase

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
        yaml.explicit_start = True
        yaml.preserve_quotes = True
        return yaml

    @staticmethod
    def extensions() -> Tuple[str, ...]:
        """Return support YAML file extensions."""
        return ('yaml', 'yml')

    def load_config(self, filepath: str) -> Dict[str, Any]:
        """Load settings from YAML configuration."""
        logging.info('loading YAML configuration file %s', filepath)
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding=self.encoding) as file:
                yaml = self.__yaml_parser(self.kind or 'safe')
                content = yaml.load(file)
        else:
            content = {}
        return content

    def dump_config(self, content: Dict[str, Any], filepath: str) -> None:
        """Save settings to YAML configuration."""
        try:
            with open(filepath, 'w', encoding=self.encoding) as file:
                yaml = self.__yaml_parser(self.kind or 'rt')
                yaml.dump(content, file)
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise
