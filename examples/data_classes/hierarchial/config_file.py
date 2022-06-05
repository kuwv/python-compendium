# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
# type: ignore
"""Example YAML config."""

import os
from dataclasses import InitVar, dataclass, field

from compendium.loader import ConfigFile

# TODO: currently dataclass and userdata is disjointed


class Item:
    def __init__(name: str) -> None:
        self.__name = name 

    @property
    def name(self) -> str:
        return self.__name


@dataclass
class Bar:
    config: InitVar['ConfigFile']
    baz: str = field(init=False)

    def __post_init__(self, config: ConfigFile) -> None:
        self.baz = config.lookup('foo.bar')

    
@dataclass
class Foo:
    config: InitVar['ConfigFile']
    baz: str = field(init=False)
    bar: Bar = field(init=False)

    def __post_init__(self, config: ConfigFile) -> None:
        self.bar = Bar(config=config)
        self.baz = config.lookup('foo.baz')


def show_types(obj):
    """Recursively show dict types."""
    # convert associative array
    if isinstance(obj, dict):
        obj = {
            f"{type(str(k))}:{str(k)}": show_types(v)
            for k, v in obj.items()
        }

    # convert list
    elif isinstance(obj, list):
        obj = [show_types(x) for x in obj]

    return f"{type(obj)}:{obj}"


basepath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(basepath, 'config.toml')

config = ConfigFile(filepath, separator='.')
settings = config.load()

foo = Foo(settings)
print(foo)
print(type(foo.bar))
print(type(foo.bar.baz))
