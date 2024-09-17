# Copyright (C) 2024 twyleg
import argparse

from pathlib import Path
from simple_python_app.generic_application import GenericApplication

from construction_meta_data_builder import __version__
from construction_meta_data_builder.readme_generator import generate_readmes_for_workspace


FILE_DIR = Path(__file__).parent


class Application(GenericApplication):

    def __init__(self):
        # fmt: off
        super().__init__(
            application_name="construction_meta_data_builder",
            version=__version__,
            application_config_init_enabled=False,
            logging_logfile_output_dir=Path.cwd() / ".logs/"
        )
        # fmt: on

    def add_arguments(self, argparser: argparse.ArgumentParser):
        pass

    def run(self, args: argparse.Namespace):
        generate_readmes_for_workspace(Path.cwd())


def main() -> None:
    application = Application()
    application.start()


if __name__ == "__main__":
    main()
