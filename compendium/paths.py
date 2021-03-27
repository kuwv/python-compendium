# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide settings modules.'''

import logging
import os
import platform
from dataclasses import dataclass, field
from typing import List, Optional

log = logging.getLogger(__name__)


@dataclass
class ConfigFilepaths:
    r'''Load config paths based on priority.

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

    '''
    # TODO: Implement pathlib

    application: str
    filename: str
    filetype: Optional[str] = field(init=False)
    root_dir: str = os.sep

    enable_system_filepaths: bool = False
    enable_user_filepaths: bool = False
    enable_local_filepaths: bool = True
    # enable_runtime_filepaths: bool = True

    system_filepaths: List[str] = field(init=False)
    user_filepaths: List[str] = field(init=False)
    local_filepaths: List[str] = field(init=False)
    # runtime_filepaths: List[str] = field(init=False)

    def __post_init__(self) -> None:
        '''Perform post path config.'''
        if '.' in self.filename:
            self.filetype = os.path.splitext(self.filename)[1].strip('.')
        else:
            self.filetype = None
        self.system_filepaths = []
        self.user_filepaths = []
        self.local_filepaths = []
        # self.runtime_filepaths = []

        if self.enable_system_filepaths and os.name == 'posix':
            # TODO: Add windows/linux compliant service path config option
            # self.system_filepaths.append(
            #     os.path.join(self.root_dir, 'etc', self.filename)
            # )

            if self.filetype:
                self.system_filepaths.append(
                    os.path.join(
                        self.root_dir,
                        'etc',
                        self.application,
                        "config.{}".format(self.filetype),
                    )
                )

            self.system_filepaths.append(
                os.path.join(
                    self.root_dir, 'etc', self.application, self.filename
                )
            )

        if self.enable_user_filepaths:
            if platform.system() == 'Windows':
                __user_app_filepath = os.path.join('AppData', 'Local')

            if platform.system() == 'Darwin':
                __user_app_filepath = os.path.join(
                    'Library', 'Application Support',
                )

            if platform.system() == 'Linux':
                __user_app_filepath = '.config'

            self.user_filepaths.append(
                os.path.join(
                    os.path.expanduser('~'),
                    __user_app_filepath,
                    self.application,
                    self.filename,
                )
            )

            if self.filetype:
                self.user_filepaths.append(
                    os.path.join(
                        os.path.expanduser('~'),
                        ".{a}.{f}".format(a=self.application, f=self.filetype),
                    )
                )

            self.user_filepaths.append(
                os.path.join(
                    os.path.expanduser('~'),
                    ".{a}.d".format(a=self.application),
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
                        "{a}.{f}".format(a=self.application, f=self.filetype),
                    )
                )

        # if self.enable_runtime_filepaths:
        #     if self.enable_system_filepaths:
        #         self.runtime_filepaths.append(
        #             os.path.join(
        #                 self.root_dir, 'etc', 'sysconfig', self.filename
        #             )
        #         )
        #     self.runtime_filepaths.append(
        #         os.path.join(os.getcwd(), '.env')
        #     )

    @property
    def filepaths(self):
        return (
            self.system_filepaths + self.user_filepaths + self.local_filepaths
        )
