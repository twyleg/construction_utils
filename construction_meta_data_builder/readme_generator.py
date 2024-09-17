# Copyright (C) 2024 twyleg
import json
import logging
import shutil
import subprocess
from pathlib import Path
from glob import glob
from typing import List, Dict, Any, Tuple
from os import listdir
from jinja2 import FileSystemLoader, Environment

from construction_meta_data_builder.freecad_exporter import FreecadExporter

FILE_DIR = Path(__file__).parent

logm = logging.getLogger(__name__)


class Construction:

    FILENAME_CONSTRUCTION_FILE = "construction.json"

    SUBDIR_NAME_SOURCE = "source"
    SUBDIR_NAME_IMG = "img"
    SUBDIR_NAME_3D = "3d"
    SUBDIR_NAME_GCODE = "gcode"

    FILE_EXTENSIONS_SOURCE = ["FCStd"]
    FILE_EXTENSIONS_IMG = ["jpeg", "jpg", "png"]
    FILE_EXTENSIONS_3D = ["stl"]
    FILE_EXTENSIONS_GCODE = ["gcode", "3mf"]

    def __init__(self, construction_dir_path: Path) -> None:
        self.construction_dir_path = construction_dir_path
        self.construction_relative_dir_path = construction_dir_path.relative_to(construction_dir_path.parent)
        self.things_data: Dict[str, Any] = self.__read_construction_file()
        self.filepaths_source: List[Tuple[Path, Path]] = self.__read_filepaths_source()
        self.filepaths_img: List[Path] = self.__read_filepaths_img()
        self.filepaths_3d: List[Path] = self.__read_filepaths_3d()
        self.filepaths_gcode: List[Path] = self.__read_filepaths_gcode()
        self.filepath_thumbnail_image = self.filepaths_img[0] if self.filepaths_img else None

    def __find_files_by_extension_and_return_relative_path(self, dir: Path, extensions: List[str]) -> List[Path]:
        files: List[str] = []
        for extension in extensions:
            files.extend(glob(str(dir / f"*.{extension}")))
        files.sort()
        return [Path(file).relative_to(self.construction_dir_path) for file in files]

    def __read_construction_file(self) -> Dict[str, Any]:
        construction_file_filepath = self.construction_dir_path / self.FILENAME_CONSTRUCTION_FILE
        with open(construction_file_filepath, "r") as json_file:
            return json.load(json_file)

    def __generate_source_files_preview_images(self, source_files_filepaths: List[Path]) -> List[Path]:
        export_image_filepaths: List[Path] = []
        for source_file_filepath in source_files_filepaths:
            export_image_filepath = self.construction_dir_path / self.SUBDIR_NAME_IMG / f"previews/{source_file_filepath.stem}.png"
            export_image_filepaths.append(export_image_filepath.relative_to(self.construction_dir_path))
        return export_image_filepaths

    def __read_filepaths_source(self) -> List[Tuple[Path, Path]]:
        source_files_filepaths = self.__find_files_by_extension_and_return_relative_path(
            self.construction_dir_path / self.SUBDIR_NAME_SOURCE, self.FILE_EXTENSIONS_SOURCE
        )
        source_file_preview_images_filepaths = self.__generate_source_files_preview_images(source_files_filepaths)
        return [
            (source_file_filepath, source_file_preview_image_filepath)
            for source_file_filepath, source_file_preview_image_filepath in zip(source_files_filepaths, source_file_preview_images_filepaths)
        ]

    def __read_filepaths_img(self) -> List[Path]:
        return self.__find_files_by_extension_and_return_relative_path(self.construction_dir_path / self.SUBDIR_NAME_IMG, self.FILE_EXTENSIONS_IMG)

    def __read_filepaths_3d(self) -> List[Path]:
        return self.__find_files_by_extension_and_return_relative_path(self.construction_dir_path / self.SUBDIR_NAME_3D, self.FILE_EXTENSIONS_3D)

    def __read_filepaths_gcode(self) -> List[Path]:
        return self.__find_files_by_extension_and_return_relative_path(self.construction_dir_path / self.SUBDIR_NAME_GCODE, self.FILE_EXTENSIONS_GCODE)


class Workspace:
    def __init__(self, workspace_dir_path: Path) -> None:
        self.workspace_dir_path = workspace_dir_path
        self.constructions = self.__find_constructions()

    def __find_constructions(self) -> List[Construction]:
        workspace_element_paths = [self.workspace_dir_path / elem for elem in listdir(self.workspace_dir_path)]
        workspace_element_paths.sort()
        constructions: List[Construction] = []
        for workspace_element_path in workspace_element_paths:
            if workspace_element_path.is_dir() and (workspace_element_path / "construction.json").exists():
                constructions.append(Construction(workspace_element_path))
        return constructions


class ReadmeGenerator:

    def __init__(self, output_dir_path: Path, template_file_path: Path, **kwargs) -> None:
        self._output_dir_path = output_dir_path
        self._template_file_path = template_file_path
        self._kwargs = kwargs

    def generate(self):
        environment = Environment(loader=FileSystemLoader(self._template_file_path.parent))
        template = environment.get_template(self._template_file_path.name)
        content = template.render(**self._kwargs)

        with open(self._output_dir_path / "README.md", mode="w", encoding="utf-8") as readme_file:
            readme_file.write(content)


class WorkspaceReadmeGenerator(ReadmeGenerator):
    def __init__(self, workspace: Workspace) -> None:
        super().__init__(workspace.workspace_dir_path, FILE_DIR / "resources/templates/template_workspace_readme.md.jinja", workspace=workspace)
        self.__create_generic_images(workspace.workspace_dir_path)

    @staticmethod
    def __create_generic_images(workspace_dir_path: Path) -> None:
        generic_img_dir_path = workspace_dir_path / ".resources/img"
        generic_img_dir_path.mkdir(parents=True, exist_ok=True)

        no_image_available_file_path_src = FILE_DIR / "resources/img/no_image_available.png"
        no_image_available_file_path_dst = generic_img_dir_path / "no_image_available.png"
        if not no_image_available_file_path_dst.exists():
            shutil.copy(no_image_available_file_path_src, no_image_available_file_path_dst)


class ConstructionReadmeGenerator(ReadmeGenerator):
    def __init__(self, construction: Construction) -> None:
        super().__init__(construction.construction_dir_path, FILE_DIR / "resources/templates/template_construction_readme.md.jinja", construction=construction)


def generate_readmes_for_workspace(workspace_path: Path) -> None:
    workspace = Workspace(workspace_path)
    logm.info("Workspace: %s", workspace_path)
    logm.info("Number of available constructions: %d", len(workspace.constructions))

    freecad_exporter = FreecadExporter()

    logm.info("Generate construction READMES:")
    for construction in workspace.constructions:
        logm.info("- %s", construction.construction_dir_path)
        construction_readme_generator = ConstructionReadmeGenerator(construction)
        construction_readme_generator.generate()
        for source_file_path, preview_file_path in construction.filepaths_source:
            freecad_exporter.add_export_job(construction.construction_dir_path / source_file_path, construction.construction_dir_path / preview_file_path)

    freecad_exporter.export()

    logm.info("Generate workspace README: %s", workspace.workspace_dir_path)
    workspace_readme_generator = WorkspaceReadmeGenerator(workspace)
    workspace_readme_generator.generate()
