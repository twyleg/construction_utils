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
    name="construction_meta_data_builder",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Torsten Wylegala",
    author_email="mail@twyleg.de",
    description="README file generator for FreeCAD construction workspaces.",
    license="GPL 3.0",
    keywords="FreeCAD Export Constructions Generator",
    url="https://github.com/twyleg/construction_meta_data_builder",
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
            "construction_meta_data_builder = construction_meta_data_builder.main:main",
        ]
    },
)
