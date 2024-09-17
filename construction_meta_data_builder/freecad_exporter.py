# Copyright (C) 2024 twyleg
import logging
import os.path
import subprocess
from typing import List, Tuple
from shutil import which
from pathlib import Path


FILE_DIR = Path(__file__).parent
logm = logging.getLogger(__name__)


class FreecadExporter:

    MODIFICATION_TIME_REQUIRED_DELTA = 2.0

    def __init__(self) -> None:
        self._export_jobs: List[Tuple[Path, Path | None]] = []

    @staticmethod
    def __is_xvfb_available() -> bool:
        return which("xvfb-run") is not None

    @staticmethod
    def __is_file_dirty(input_file_path: Path, output_file_path: Path) -> bool:
        if output_file_path.exists():
            return os.path.getmtime(input_file_path) - os.path.getmtime(output_file_path) > FreecadExporter.MODIFICATION_TIME_REQUIRED_DELTA
        else:
            return True

    def add_export_job(self, input_file_path: Path, output_file_or_dir_path: Path | None = None, force=False) -> None:
        if output_file_or_dir_path is None or self.__is_file_dirty(input_file_path, output_file_or_dir_path) or force:
            self._export_jobs.append((input_file_path, output_file_or_dir_path))

    def export(self) -> None:

        file_args: List[str] = []

        logm.info("Running FreeCAD export script")

        for export_job in self._export_jobs:
            input_file_path = export_job[0]
            output_file_or_dir_path = export_job[1]

            if output_file_or_dir_path:
                file_args.append(f"{input_file_path}:{output_file_or_dir_path}")
            else:
                file_args.append(str(input_file_path))

        if file_args:
            logm.info("Export jobs:")
            for file_arg in file_args:
                logm.info("- %s", file_arg)

            args: List[str] = []

            if self.__is_xvfb_available():
                logm.info("xvfb available - visual output will be redirected and hidden through xvfb.")
                args.append("xvfb-run")
                args.append("-a")
            else:
                logm.info("xvfb NOT available - unable to hide visual output.")

            args.append("freecad")
            args.append(str(FILE_DIR / "resources/scripts/freecad_export_image_script.py"))
            args.append("--pass")
            args.extend(file_args)

            logm.debug("FreeCAD command: %s", " ".join(args))
            completed_process = subprocess.run(args, capture_output=True)
            try:
                for line in completed_process.stdout.decode("utf-8").splitlines():
                    logm.debug(line)
                logm.info("Export done!")
            except subprocess.CalledProcessError as e:
                logm.error("Export failed!")
                logm.exception(e)
        else:
            logm.info("No FreeCAD export jobs available.")
