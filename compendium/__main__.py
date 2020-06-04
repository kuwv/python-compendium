from .settings import Settings
from .cli import cli
import os

conpend_home = os.environ.get("COMPEND_HOME")
conpend_conf = os.environ.get("COMPEND_CONF")
conpend_log = os.environ.get("COMPEND_LOG")

controller = Settings(
    filename="lunar.yml",
    config_dir="tests/conf",
    home_dir=".",
    log_dir="logs",
)


def main():
    print(controller.get_settings())
