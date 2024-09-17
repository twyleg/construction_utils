# Copyright (C) 2024 twyleg
import shutil

import pytest

import logging
from pathlib import Path

from construction_meta_data_builder.readme_generator import Construction, Workspace, ConstructionReadmeGenerator, WorkspaceReadmeGenerator

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
    workspace_template_filepath = FILE_DIR / "resources/workspaces/example_construction_workspace"
    dst_workspace_filepath = tmp_path / "construction_workspace"
    shutil.copytree(workspace_template_filepath, dst_workspace_filepath)
    monkeypatch.chdir(dst_workspace_filepath)
    return dst_workspace_filepath


class TestConstructionReader:
    def test_ValidConstruction_ReadConstruction_ConstructionReadSuccessfully(self, caplog, workspace):
        construction = Construction(workspace / "construction_a")

        assert construction.things_data["name"] == "Construction A"
        assert construction.things_data["tags"][0] == "construction"
        assert construction.things_data["tags"][1] == "a"
        assert construction.things_data["thingiverse_id"] == 0
        assert construction.things_data["thingiverse_creator"] == "creator"

        assert len(construction.filepaths_source) == 3
        assert len(construction.filepaths_img) == 3
        assert len(construction.filepaths_3d) == 3
        assert len(construction.filepaths_gcode) == 1


class TestConstructionReadmeGenerator:
    def test_ValidConstructionWorkspace_GenerateConstructionReadme_ReadmeGenerated(self, caplog, workspace):
        construction_dir = workspace / "construction_a"
        construction = Construction(construction_dir)
        construction_readme_generator = ConstructionReadmeGenerator(construction)
        construction_readme_generator.generate()


class TestWorkspaceReadmeGenerator:
    def test_ValidConstructionWorkspace_GenerateWorkspaceReadme_ReadmeGenerated(self, caplog, workspace):
        construction_workspace = Workspace(workspace)
        construction_workspace_readme_generator = WorkspaceReadmeGenerator(construction_workspace)
        construction_workspace_readme_generator.generate()
        for construction in construction_workspace.constructions:
            print(construction.construction_dir_path)
