# Copyright (C) 2024 twyleg
import json
import shutil
import subprocess
from pathlib import Path
from glob import glob
from typing import List, Dict, Any, Tuple
from os import listdir
from jinja2 import FileSystemLoader, Environment

FILE_DIR = Path(__file__).parent


class Construction:

    FILENAME_THINGS_FILE = "things.json"

    SUBDIR_NAME_SOURCE = "source"
    SUBDIR_NAME_IMG = "img"
    SUBDIR_NAME_3D = "3d"
    SUBDIR_NAME_GCODE = "gcode"

    FILE_EXTENSIONS_SOURCE = ["FCStd"]
    FILE_EXTENSIONS_IMG = ["jpeg", "jpg", "png"]
    FILE_EXTENSIONS_3D = ["stl"]
    FILE_EXTENSIONS_GCODE = []

    def __init__(self, construction_dir_path: Path):
        self.construction_dir_path = construction_dir_path
        self.construction_relative_dir_path = construction_dir_path.relative_to(construction_dir_path.parent)
        self.things_data: Dict[str, Any] = self.__read_things_file()
        self.filepaths_source: List[Tuple[Path, Path]] = self.__read_filepaths_source()
        self.filepaths_img: List[Path] = self.__read_filepaths_img()
        self.filepaths_3d: List[Path] = self.__read_filepaths_3d()
        self.filepaths_gcode: List[Path] = self.__read_filepaths_gcode()
        self.filepath_thumbnail_image = self.filepaths_img[0]

    def __find_files_by_extension_and_return_relative_path(self, dir: Path, extensions: List[str]) -> List[Path]:
        files: List[str] = []
        for extension in extensions:
            files.extend(glob(str(dir / f"*.{extension}")))
        return [Path(file).relative_to(self.construction_dir_path) for file in files]

    def __read_things_file(self) -> Dict[str, Any]:
        things_file_filepath = self.construction_dir_path / self.FILENAME_THINGS_FILE
        with open(things_file_filepath, 'r') as json_file:
            return json.load(json_file)

    def __generate_source_files_preview_images(self, source_files_filepaths: List[Path]) -> List[Path]:
        export_image_filepaths: List[Path] = []
        for source_file_filepath in source_files_filepaths:
            subprocess.run([
                "xvfb-run",
                "freecad",
                "-u",
                FILE_DIR / "resources/freecad_no_splash_user.cfg",
                self.construction_dir_path / source_file_filepath,
                FILE_DIR / "resources/freecad_export_image.py"
            ])
            export_image_filepath = self.construction_dir_path / self.SUBDIR_NAME_SOURCE / f"{source_file_filepath.stem}.png"
            shutil.move(Path.cwd() / "image.png", export_image_filepath)
            export_image_filepaths.append(export_image_filepath.relative_to(self.construction_dir_path))
        return export_image_filepaths

    def __read_filepaths_source(self) -> List[Tuple[Path, Path]]:
        source_files_filepaths = self.__find_files_by_extension_and_return_relative_path(self.construction_dir_path / self.SUBDIR_NAME_SOURCE,
                                                                self.FILE_EXTENSIONS_SOURCE)
        source_file_preview_images_filepaths = self.__generate_source_files_preview_images(source_files_filepaths)

        source_files_filepaths.sort()
        source_file_preview_images_filepaths.sort()
        return [(source_file_filepath, source_file_preview_image_filepath) for source_file_filepath, source_file_preview_image_filepath in zip(source_files_filepaths, source_file_preview_images_filepaths)]

    def __read_filepaths_img(self) -> List[Path]:
        return self.__find_files_by_extension_and_return_relative_path(self.construction_dir_path / self.SUBDIR_NAME_IMG,
                                                                       self.FILE_EXTENSIONS_IMG)

    def __read_filepaths_3d(self) -> List[Path]:
        return self.__find_files_by_extension_and_return_relative_path(self.construction_dir_path / self.SUBDIR_NAME_3D,
                                                                       self.FILE_EXTENSIONS_3D)

    def __read_filepaths_gcode(self) -> List[Path]:
        return self.__find_files_by_extension_and_return_relative_path(self.construction_dir_path / self.SUBDIR_NAME_GCODE,
                                                                       self.FILE_EXTENSIONS_GCODE)


class Workspace:
    def __init__(self, workspace_dir_path: Path):
        self.workspace_dir_path = workspace_dir_path
        self.constructions = self.__find_constructions()

    def __find_constructions(self) -> List[Construction]:
        workspace_element_paths = [self.workspace_dir_path / elem for elem in listdir(self.workspace_dir_path)]
        workspace_element_paths.sort()
        constructions: List[Construction] = []
        for workspace_element_path in workspace_element_paths:
            if workspace_element_path.is_dir() and (workspace_element_path / "things.json").exists():
                constructions.append(Construction(workspace_element_path))
        return constructions


class WorkspaceReadmeGenerator:

    def __init__(self, workspace: Workspace):
        self._workspace = workspace

    def generate(self, output_dir: Path):
        environment = Environment(loader=FileSystemLoader(FILE_DIR / "resources"))
        template = environment.get_template("template_workspace_readme.md.jinja")
        content = template.render(
            workspace=self._workspace
        )

        with open(output_dir / "README.md", mode="w", encoding="utf-8") as readme_file:
            readme_file.write(content)


class ConstructionReadmeGenerator:

    def __init__(self, construction: Construction):
        self._construction = construction

    def generate(self, output_dir: Path):
        environment = Environment(loader=FileSystemLoader(FILE_DIR / "resources"))
        template = environment.get_template("template_construction_readme.md.jinja")
        content = template.render(
            construction=self._construction
        )

        with open(output_dir / "README.md", mode="w", encoding="utf-8") as readme_file:
            readme_file.write(content)
