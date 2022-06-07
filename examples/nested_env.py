# type: ignore
"""Provide example environs usage."""

import os
from pprint import pprint

from compendium.settings import Environs

key = 'COMPEND_EXAMPLE_DATA'
value = 12

config1 = {
    'proman': {
        'name': 'app1',
        'version': '1.2.3',
        'description': 'this is an example',
        'defaults': {
            'enable_feature': False
        }
    }
}

config2 = {
    'tool': {
        'proman': {
            'enable_feature': True,
            'settings': {
                'files': [
                    {'path': '/some/path/to/file', 'kind': 'yaml'}
                ],
                'writable': True
            }
        },
        'example': {
             'version': '1.2.4.dev0'
        }
    }
}

os.environ[key, str(value)]
print(os.getenv(key))
environs = Environs(config1, config2)
pprint(environs.data)
# pprint(environs.to_dict(key, value))

assert {'compend': {'example': {'data': 12}}} == environs.to_dict(key, value)
