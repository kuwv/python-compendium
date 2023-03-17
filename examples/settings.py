# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide query capabilities."""

import logging
import os

from compendium.settings import Settings

log = logging.getLogger(__name__)


if __name__ == '__main__':
    basedir = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(basedir, 'config.toml')

    settings = Settings(
        {
            'compend': {'example': {'data': 12}},
            'servers': [
                {'name': 'alpha', 'ip': '10.0.0.1', 'dc': 'eqdc10'},
                {'name': 'beta', 'ip': '10.0.0.2', 'dc': 'eqdc10'},
            ],
        }
    )

    # __getitem__
    print('__getitem__', settings['/compend/example/data'])

    # get()
    print('get()', settings.get('/nada/does/not/exist', 'yey'))

    # pop()
    print('pop()', settings.pop('/compend'))
    print('pop()', settings.pop('/nada/does/not/exist', 'yey'))

    # values()
    print('values', settings.values())
    print('values', settings.values('/servers/**/ip'))

    # __setitem__
    settings['/foo'] = 'bar'
    print('__setitem__', settings['/foo'])

    # __contains__
    print('foo' in settings)
    print('contains', settings)

    # update
    settings.update({'update': {'tickets': True}})
    print('update', settings)

    print(vars(settings))
    print(len(settings))
    print(settings.keys())
    for k, v in settings.items():
        print('- keypath', k)
        print('- value', v)

    del settings['/servers']
    print(settings)
    settings.clear()
    print(settings)
