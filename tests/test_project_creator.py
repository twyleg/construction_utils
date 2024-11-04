# Copyright (C) 2024 twyleg
import shutil

import pytest

import logging
from pathlib import Path

from construction_utils.project_creator import create_project

#
# General naming convention for unit tests:
#               test_INITIALSTATE_ACTION_EXPECTATION
#


FILE_DIR = Path(__file__).parent


@pytest.fixture(autouse=True)
def print_tmp_path(tmp_path):
    logging.info("tmp_path: %s", tmp_path)
    return None


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    workspace_dirpath = tmp_path / "construction_workspace"
    workspace_dirpath.mkdir()
    monkeypatch.chdir(workspace_dirpath)
    return workspace_dirpath


class TestProjectCreator:
    @staticmethod
    def assert_file_contains_string(filepath: Path, expected_string: str):
        with open(filepath, "r") as file:
            content = file.read()
        assert expected_string in content

    def test_ValidConstructionWorkspace_CreateNewProject_ProjectStructureCreated(self, caplog, workspace):
        project_name = "test_project"
        create_project(workspace, project_name)

        project_dir = workspace / project_name

        expected_files = [
            "source/.gitignore",
            "3d/.gitignore",
            "img/.gitignore",
            "gcode/.gitignore",
            "resources/.gitignore",
            "resources/origins.csv",
            "construction.json",

        ]

        for expected_file in expected_files:
            expected_file_path = project_dir / expected_file
            assert expected_file_path.exists()

        self.assert_file_contains_string(project_dir / "construction.json", '"name": "test_project",')
