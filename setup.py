# Copyright (C) 2024 twyleg
import versioneer
from pathlib import Path
from setuptools import find_packages, setup


def read(relative_filepath):
    return open(Path(__file__).parent / relative_filepath).read()


def read_long_description() -> str:
    return read("README.md")


# fmt: off
setup(
    name="construction_utils",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Torsten Wylegala",
    author_email="mail@twyleg.de",
    description="Utilities for FreeCAD construction workspaces.",
    license="GPL 3.0",
    keywords="FreeCAD Export Constructions Generator Utilities",
    url="https://github.com/twyleg/construction_utils",
    packages=find_packages(),
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        "simple-python-app",
        "jinja2~=3.1.4"
    ],
    entry_points={
        "console_scripts": [
            "construction_utils = construction_utils.main:main",
        ]
    },
)
