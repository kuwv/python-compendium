from .settings import Settings
from .cli import cli

controllers = Settings(scenario='default').get_settings().get('controllers')
self.load_scenarios(controllers)

def main():
    print(self.__controllers)
