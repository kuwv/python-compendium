# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
'''Test settings management.'''

import os

import pytest  # type: ignore

from compendium.config_manager import ConfigManager

config_path = os.path.dirname(os.path.realpath(__file__))
settings_path = config_path + '/settings.toml'


# @pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_toml_delete():  # fs):
    '''Test content deletion.'''
    # fs.add_real_file(settings_path, False)
    cfg = ConfigManager(
        application='tests',
        configs=[{'filename': 'settings.toml', 'path': settings_path}],
    )
    # cfg.load()
    # assert cfg.search('/owner/name') == ['Tom Preston-Werner']
    # cfg.delete('/owner/name')
    # assert cfg.search('/owner/name') == []
    cfg.stop_all()
