# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide settings modules."""

import logging
import os
import platform
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

log = logging.getLogger(__name__)


@dataclass
class File:
    path: str
    name: str = field(init=False)
    extension: Optional[str] = field(init=False)

    def __post_init__(self) -> None:
        """Intialize filepath."""
        self.name = os.path.basename(self.filepath) or 'config.toml'

        if '.' in self.name and not self.name.startswith('.'):
            self.extension = os.path.splitext(self.name)[-1].strip('.')
        else:
            self.extension = 'toml'


@dataclass
class ConfigPaths:
    r"""Load config paths based on priority.

    First(lowest) to last(highest):
      1. Load config.<FILETYPE> from /etc/<APP>
        - /etc/<FILENAME>
        - /etc/<APP>/config.<FILETYPE>
        - /etc/<APP>/<FILENAME>
      2. Load user configs
        - Windows: ~\\AppData\\Local\\<COMPANY>\\<APP>\\<FILENAME>
        - Darwin: ~/Library/Application Support/<APP>/<FILENAME>
        - Linux: ~/.config/<APP>/<FILENAME>
        - ~/.<APP>.<FILETYPE>
        - ~/.<APP>.d/<FILENAME>
      3. Load config in PWD
        - ./config.<FILETYPE>
        - ./<FILENAME>
      4. Runtime configs:
        - /etc/sysconfig/<APP>
        - .env
        - <CLI>

    """

    # TODO: Implement pathlib

    name: str
    filename: str
    filetype: Optional[str] = field(init=False)
    basedir: str = os.sep

    enable_system_filepaths: bool = False
    enable_global_filepaths: bool = False
    enable_local_filepaths: bool = True
    # enable_runtime_filepaths: bool = True

    system_filepaths: List[str] = field(init=False)
    global_filepaths: List[str] = field(init=False)
    local_filepaths: List[str] = field(init=False)
    # runtime_filepaths: List[str] = field(init=False)

    def __post_init__(self) -> None:
        """Perform post path config."""
        if '.' in self.filename:
            self.filetype = os.path.splitext(self.filename)[1].strip('.')
        else:
            self.filetype = None
        self.system_filepaths = []
        self.global_filepaths = []
        self.local_filepaths = []
        # self.runtime_filepaths = []

        if self.enable_system_filepaths and os.name == 'posix':
            # TODO: Add windows/linux compliant service path config option
            # self.system_filepaths.append(
            #     os.path.join(self.basedir, 'etc', self.filename)
            # )

            if self.filetype:
                self.system_filepaths.append(
                    os.path.join(
                        self.basedir,
                        'etc',
                        self.name,
                        f"config.{self.filetype}",
                    )
                )

            self.system_filepaths.append(
                os.path.join(self.basedir, 'etc', self.name, self.filename)
            )

        if self.enable_global_filepaths:
            if platform.system() == 'Windows':
                __global_app_filepath = os.path.join('AppData', 'Local')

            if platform.system() == 'Darwin':
                __global_app_filepath = os.path.join(
                    'Library', 'Application Support',
                )

            if platform.system() == 'Linux':
                __global_app_filepath = '.config'

            self.global_filepaths.append(
                os.path.join(
                    os.path.expanduser('~'),
                    __global_app_filepath,
                    self.name,
                    self.filename,
                )
            )

            if self.filetype:
                self.global_filepaths.append(
                    os.path.join(
                        os.path.expanduser('~'),
                        f".{self.name}.{self.filetype}",
                    )
                )

            self.global_filepaths.append(
                os.path.join(
                    os.path.expanduser('~'),
                    f".{self.name}.d",
                    self.filename,
                )
            )

        if self.enable_local_filepaths:
            self.local_filepaths.append(
                os.path.join(os.getcwd(), self.filename)
            )
            if self.filetype:
                self.local_filepaths.append(
                    os.path.join(
                        os.getcwd(),
                        f"{self.name}.{self.filetype}",
                    )
                )

        # if self.enable_runtime_filepaths:
        #     if self.enable_system_filepaths:
        #         self.runtime_filepaths.append(
        #             os.path.join(
        #                 self.basedir, 'etc', 'sysconfig', self.filename
        #             )
        #         )
        #     self.runtime_filepaths.append(
        #         os.path.join(os.getcwd(), '.env')
        #     )

    @property
    def filepaths(self) -> Tuple[str, ...]:
        """Return combined list of all paths."""
        return tuple(
            self.system_filepaths
            + self.global_filepaths
            + self.local_filepaths
        )
