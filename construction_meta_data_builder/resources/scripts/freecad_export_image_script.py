"""
Copyright (C) 2024 twyleg

FreeCAD image export script.

Input: .FCStd file
Output: Isometric, Orthographic view in PNG format

Usage:
    freecad freecad_export_image.py --pass <input_file_path_0>[:<output_dir/[output_filename.png]] [<input_file_path_1...]

Examples:
- Single input file:
    Command: freecad freecad_export_image.py --pass source/example_0.FCStd
    Result: source/example_0.FCStd -> source/example_0.png

- Single input file with explicit output dir:
    Command: freecad freecad_export_image.py --pass source/example_0.FCStd:output/
    Result: source/example_0.FCStd -> output/example_0.png

- Single input file with explicit output file path:
    Command: freecad freecad_export_image.py --pass source/example_0.FCStd:output/example_output_0.png
    Result: source/example_0.FCStd -> output/example_output_0.png

- Multiple input files with and without explicit output dirs and file path:
    Command: freecad freecad_export_image.py --pass source/example_0.FCStd source/example_1.FCStd:output_1/ source/example_2.FCStd:output_2/example_output_2.png
    Results:
        -source/example_0.FCStd -> source/example_0.png
        -source/example_1.FCStd -> output_1/example_1.png
        -source/example_2.FCStd -> output_2/example_output_2.png
"""

import sys
from typing import List, Tuple, Union

import FreeCADGui as Gui  # type: ignore
import FreeCAD  # type: ignore

from pathlib import Path


def get_script_args() -> List[str]:
    def list_split(l, element):
        if l[-1] == element:
            return l, []
        delimiter = l.index(element) + 1
        return l[:delimiter], l[delimiter:]

    return list_split(sys.argv, "--pass")[1]


def get_input_output_file_paths_pairs(args: List[str]) -> List[Tuple[Path, Union[Path, None]]]:
    input_output_file_paths_pairs: List[Tuple[Path, Union[Path, None]]] = []
    for arg in args:
        if ":" in arg:
            splitted_arg = arg.split(":")
            input_file_path = Path(splitted_arg[0])
            output_file_path = Path(splitted_arg[1])
            input_output_file_paths_pairs.append((input_file_path, output_file_path))
        else:
            input_file_path = Path(arg)
            output_file_path = None
            input_output_file_paths_pairs.append((input_file_path, output_file_path))
    return input_output_file_paths_pairs


print(f"sys.argv: {sys.argv}")

script_args = get_script_args()
input_output_file_path_pairs = get_input_output_file_paths_pairs(script_args)

for input_output_file_path_pair in input_output_file_path_pairs:

    input_file_path = input_output_file_path_pair[0]
    output_file_path = input_output_file_path_pair[1]

    if output_file_path is None:
        output_file_path = input_file_path.parent / f"{input_file_path.stem}.png"
    elif output_file_path.suffix:
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_file_path.mkdir(parents=True, exist_ok=True)
        output_file_path = output_file_path / f"{input_file_path.stem}.png"

    print(f"Exporting PNG:  {input_file_path} -> {output_file_path}")

    doc = FreeCAD.openDocument(str(input_file_path))

    Gui.SendMsgToActiveView("OrthographicCamera")
    Gui.SendMsgToActiveView("ViewAxo")

    view = Gui.ActiveDocument.ActiveView
    view.saveImage(str(output_file_path), 1000, 1000, "White")

    FreeCAD.closeDocument(doc.Name)

Gui.doCommand("exit()")
