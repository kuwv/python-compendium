from collections import UserDict

from compendium.settings import EnvironsMixin

key = 'COMPEND_EXAMPLE_DATA'
value = 12


class Environs(UserDict, EnvironsMixin):
    def __init__(self, *args):
        self.prefix = 'COMPEND'
        super().__init__(*args)

    def __repr__(self):
        return repr(Environs.environs)


environs = Environs()
environs.load_dotenv()
environs.load_environs()
print('environs', environs.environs)
print('example to_dict', environs.to_dict(key, value))
