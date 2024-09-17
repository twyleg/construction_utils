[![Build status](https://github.com/twyleg/construction_meta_data_builder/actions/workflows/tests.yaml/badge.svg)]()
[![GitHub latest commit](https://badgen.net/github/last-commit/twyleg/construction_meta_data_builder)](https://GitHub.com/twyleg/construction_meta_data_builder/commit/)
[![PyPI download month](https://img.shields.io/pypi/dm/template-project-python)](https://pypi.python.org/pypi/constructions-meta-data-builder/)
[![PyPi version](https://badgen.net/pypi/v/template-project-python/)](https://pypi.org/project/constructions-meta-data-builder)


# construction_meta_data_builder

The construction meta data builder generates README files for FreeCAD workspaces.
Its main goal is to serve for my personal [constructions](https://github.com/twyleg/constructions) repo. 

## Installation

    cd construction_workspace/
    python -m venv venv
    venv/bin/activate

    pip install construction_meta_data_builder

## Usage

    cd construction_workspace/
    construction_meta_data_builder

## System dependencies

The following packages need to be installed and made available to the user that runs the construction_meta_data_builder.

* freecad
* xvfb (to run freecad headless)

## Examples

Check [constructions](https://github.com/twyleg/constructions) repo for a productive example project.

## Caveats

* **Ubuntu/Snap based distribution**: 
    * The construction_meta_data_builder requires FreeCAD to generate isometric preview images of constructions.
    * On snap based distributions it is likely that FreeCAD is installed via snap.
    * Snap applications run in a sandbox and therefore have their own private */tmp/* directory and won't be able to access the systems */tmp/* directory.
    * Unittest rely heavily on the tmp dir. Therefor it is necessary to use pytests **--basetemp=\<PATH\>** argument to pass a custom temp directory to pytest.
    * In tox we're using **.pytest_tmp/**