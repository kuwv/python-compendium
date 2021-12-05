# type: ignore
"""Provide example environs usage."""
from collections import UserDict

from compendium.settings import EnvironsMixin

key = 'COMPEND_EXAMPLE_DATA'
value = 12


class Environs(UserDict, EnvironsMixin):
    """Provide environs object."""

    def __init__(self, *args):
        """Initialize environs."""
        self.prefix = 'COMPEND'
        super().__init__(*args)

    def __repr__(self):
        """Provide string representation of environs."""
        return repr(Environs)


environs = Environs()
environs.load_dotenv()
environs.load_environs()
print('environs', environs)
print('example to_dict', environs.to_dict(key, value))
assert {'compend': {'example': {'data': 12}}} == environs.to_dict(key, value)
