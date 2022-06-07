# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
# type: ignore
"""Example YAML config."""

import os
from compendium.loader import ConfigFile

basepath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(basepath, 'example.yaml')

cfg = ConfigFile(writable=True, factory_kwargs={'separator': '.'})
settings = cfg.load(filepath=filepath)
print(settings.separator)

print('settings', settings)
