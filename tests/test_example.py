# Copyright (C) 2024 twyleg
import shutil

import pytest

import logging
from pathlib import Path

from construction_meta_data_builder.main import Application

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


@pytest.fixture()
def valid_config_file(tmp_path):
    config_template_filepath = FILE_DIR / "resources/configs/valid_construction_meta_data_builder_config.json"
    dst_workspace_filepath = tmp_path / "construction_workspace"
    dst_workspace_filepath.mkdir(exist_ok=True)
    dst_config_filepath = dst_workspace_filepath / "construction_meta_data_builder_config.json"
    shutil.copy(config_template_filepath, dst_config_filepath)
    return dst_config_filepath


class TestExample:
    def test_ValidreferenceLightMatrix_Read_Success(self, caplog, workspace, valid_config_file):
        app = Application()
        app.start([])
