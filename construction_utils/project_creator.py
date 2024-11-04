# Copyright (C) 2024 twyleg
import logging
import shutil
from pathlib import Path
from jinja2 import FileSystemLoader, Environment


FILE_DIR = Path(__file__).parent

logm = logging.getLogger(__name__)


def __create_subdirs(project_dir_path: Path) -> None:
    dir_names_to_create = [
        "source",
        "3d",
        "resources",
        "img",
        "gcode"
    ]

    logm.debug("Creating project subdirs/files:")

    for dir_name_to_create in dir_names_to_create:
        dir_path_to_create = project_dir_path / dir_name_to_create
        logm.debug("  - Dir: %s", dir_path_to_create)
        dir_path_to_create.mkdir()

        gitignore_file_path_to_create = dir_path_to_create / ".gitignore"
        logm.debug("  - File: %s", gitignore_file_path_to_create)
        gitignore_file_path_to_create.touch()


def __create_resource_origins_file(project_dir_path: Path) -> None:
    src_file = FILE_DIR / "resources/templates/origins.csv"
    dst_file = project_dir_path / "resources/origins.csv"
    logm.debug("Copying origins.csv template to \"%s\"", dst_file)
    shutil.copy(src_file, dst_file)


def __create_construction_file(project_dir_path: Path, project_name: str) -> None:
    environment = Environment(loader=FileSystemLoader(FILE_DIR / "resources/templates/"))
    template = environment.get_template("template_construction.json.jinja")
    content = template.render(name=project_name)

    construction_file_path = project_dir_path / "construction.json"
    logm.debug("Creating construction.json from tempalte: %s", construction_file_path)
    with open(construction_file_path, mode="w", encoding="utf-8") as construction_file:
        construction_file.write(content)


def create_project(root_dir_path: Path, project_name: str) -> None:
    project_dir_path = root_dir_path / project_name

    logm.info("Creating project: name=\"%s\", workspace=\"%s\"", project_name, root_dir_path)
    
    if project_dir_path.exists():
        logm.warning("Destination project directory (\"%s\") already existing. Abort!", project_dir_path.absolute())
        return

    logm.debug("Creating project dir: %s", project_dir_path)
    project_dir_path.mkdir()

    __create_subdirs(project_dir_path)
    __create_resource_origins_file(project_dir_path)
    __create_construction_file(project_dir_path, project_name)
