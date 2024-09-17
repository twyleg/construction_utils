# Copyright (C) 2024 twyleg
import shutil

import pytest

import logging
from pathlib import Path

from construction_meta_data_builder.freecad_exporter import FreecadExporter


FILE_DIR = Path(__file__).parent


@pytest.fixture
def workspace(tmp_path):
    source_dir_filepath = FILE_DIR / "resources/src"
    dst_workspace_filepath = tmp_path / "src/"
    shutil.copytree(source_dir_filepath, dst_workspace_filepath)
    return tmp_path


class TestConstructionReadmeGenerator:

    def file_exists(self, file_path: Path) -> bool:
        return file_path.exists() and file_path.is_file()

    def test_ValidSourceFiles_AddExportJobsInMultipleFormats_ImagesExported(self, caplog, workspace):
        freecad_exporter = FreecadExporter()
        freecad_exporter.add_export_job(workspace / "src/example_part_a.FCStd")
        freecad_exporter.add_export_job(workspace / "src/example_part_b.FCStd", workspace / "output_b/")
        freecad_exporter.add_export_job(workspace / "src/example_part_c.FCStd", workspace / "output_c/example_output_part_c.png")

        freecad_exporter.export()

        assert self.file_exists(workspace / "src/example_part_a.png")
        assert self.file_exists(workspace / "output_b/example_part_b.png")
        assert self.file_exists(workspace / "output_c/example_output_part_c.png")
