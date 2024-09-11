# Copyright (C) 2024 twyleg
import argparse

from pathlib import Path
from simple_python_app.generic_application import GenericApplication

from construction_meta_data_builder import __version__


FILE_DIR = Path(__file__).parent


class Application(GenericApplication):

    def __init__(self):
        # fmt: off
        super().__init__(
            application_name="construction_meta_data_builder",
            version=__version__,
            application_config_schema_filepath=FILE_DIR / "resources/application_config_schema.json"
        )
        # fmt: on

    def add_arguments(self, argparser: argparse.ArgumentParser):
        self.logm.info("init_argparse()")

        argparser.add_argument("--example", type=str, default=None, help="Example")

    def run(self, args: argparse.Namespace):
        self.logm.info("run()")
        self.logm.debug("run()")

        self.logm.info("Config: %s", self.application_config)
        self.logm.info("cwd: %s", Path.cwd())


def main() -> None:
    application = Application()
    application.start()


if __name__ == "__main__":
    main()
