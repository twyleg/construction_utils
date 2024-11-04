# Copyright (C) 2024 twyleg
import argparse

from pathlib import Path
from simple_python_app.subcommand_application import SubcommandApplication

from construction_utils import __version__
from construction_utils.readme_generator import generate_readmes_for_workspace
from construction_utils.project_creator import create_project


FILE_DIR = Path(__file__).parent


class Application(SubcommandApplication):

    def __init__(self):
        # fmt: off
        super().__init__(
            application_name="construction_utils",
            version=__version__,
            application_config_init_enabled=False,
            logging_logfile_output_dir=Path.cwd() / ".logs/"
        )
        # fmt: on

    def add_arguments(self, argparser: argparse.ArgumentParser):
        # fmt: off
        generate_docs_command = self.add_subcommand(
            command="generate_docs",
            help="Generate documentation (READMEs) for for this workspace.",
            description="Generate documentation (READMEs) for for this workspace.",
            handler=self.handle_generate_docs
        )
        create_project_command = self.add_subcommand(
            command="create_project",
            help="Create a new project with default file structure.",
            description="Create a new project with default file structure.",
            handler=self.handle_create_project
        )

        create_project_command.parser.add_argument(
            "project_name",
            type=str,
            help="Name of the project",
        )
        # fmt: on

    def handle_generate_docs(self, args: argparse.Namespace) -> int:
        generate_readmes_for_workspace(Path.cwd())
        return 0

    def handle_create_project(self, args: argparse.Namespace) -> int:
        create_project(Path.cwd(), args.project_name)
        return 0


def main() -> None:
    application = Application()
    application.start()


if __name__ == "__main__":
    main()
