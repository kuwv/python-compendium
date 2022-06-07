# type: ignore
"""Provide example environs usage."""

import os

from compendium.settings import EnvironSettings, SettingsMap

key = 'TEST_EXAMPLE_DATA'
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

# load environment variable
os.environ[key] = str(value)
assert int(os.getenv(key)) == value, 'environment variable does not exist'

environs = EnvironSettings(SettingsMap(config1, config2), prefix='TEST')

# convert key/value environs into dictionary
assert environs.to_dict(key, value) == {'test': {'example': {'data': 12}}}

# ensure converted environs do not have prefix
assert environs.environs == {'example': {'data': 12}}

assert environs['/example/data'] == 12
assert environs['/tool/proman/enable_feature'] is True
