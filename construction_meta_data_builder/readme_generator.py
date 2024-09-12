# Copyright (C) 2024 twyleg
import json
from pathlib import Path
from glob import glob
from typing import List, Dict, Any

import jinja2
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
        self.things_data: Dict[str, Any] = self.__read_things_file()
        self.filepaths_source: List[Path] = self.__read_filepaths_source()
        self.filepaths_img: List[Path] = self.__read_filepaths_img()
        self.filepaths_3d: List[Path] = self.__read_filepaths_3d()
        self.filepaths_gcode: List[Path] = self.__read_filepaths_gcode()
        self.thumbnail_image_relative_path = self.filepaths_img[0]

    def __find_files_by_extension_and_return_relative_path(self, dir: Path, extensions: List[str]) -> List[Path]:
        files: List[str] = []
        for extension in extensions:
            files.extend(glob(str(dir / f"*.{extension}")))
        return [Path(file).relative_to(self.construction_dir_path) for file in files]

    def __read_things_file(self) -> Dict[str, Any]:
        things_file_filepath = self.construction_dir_path / self.FILENAME_THINGS_FILE
        with open(things_file_filepath, 'r') as json_file:
            return json.load(json_file)

    def __read_filepaths_source(self) -> List[Path]:
        return self.__find_files_by_extension_and_return_relative_path(self.construction_dir_path / self.SUBDIR_NAME_SOURCE,
                                                                       self.FILE_EXTENSIONS_SOURCE)

    def __read_filepaths_img(self) -> List[Path]:
        return self.__find_files_by_extension_and_return_relative_path(self.construction_dir_path / self.SUBDIR_NAME_IMG,
                                                                       self.FILE_EXTENSIONS_IMG)

    def __read_filepaths_3d(self) -> List[Path]:
        return self.__find_files_by_extension_and_return_relative_path(self.construction_dir_path / self.SUBDIR_NAME_3D,
                                                                       self.FILE_EXTENSIONS_3D)

    def __read_filepaths_gcode(self) -> List[Path]:
        return self.__find_files_by_extension_and_return_relative_path(self.construction_dir_path / self.SUBDIR_NAME_GCODE,
                                                                       self.FILE_EXTENSIONS_GCODE)

class ConstructionReadmeGenerator:

    def __init__(self, construction: Construction):
        self._construction = construction

    def generate(self, output_dir: Path):
        environment = Environment(loader=FileSystemLoader(FILE_DIR / "resources"))
        template = environment.get_template("template_construction_readme.md.jinja")
        content = template.render(
            name=self._construction.things_data["name"],
            thingiverse_id=self._construction.things_data["thingiverse_id"],
            description=self._construction.things_data["thingiverse_description"],
            tags=self._construction.things_data["tags"],
            thumbnail_image=self._construction.thumbnail_image_relative_path,
            files_source=self._construction.filepaths_source,
            files_images=self._construction.filepaths_img,
            files_three_dimensionals=self._construction.filepaths_3d,
            files_gcode=self._construction.filepaths_gcode
        )

        with open(output_dir / "README.md", mode="w", encoding="utf-8") as readme_file:
            readme_file.write(content)