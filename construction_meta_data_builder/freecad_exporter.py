# Copyright (C) 2024 twyleg
import logging
import subprocess
from typing import List, Tuple
from shutil import which
from pathlib import Path


FILE_DIR = Path(__file__).parent
logm = logging.getLogger(__name__)


class FreecadExporter:

    def __init__(self):
        self._export_jobs: List[Tuple[Path, Path | None]] = []

    def add_export_job(self, input_file_path: Path, output_file_or_dir_path: Path | None = None) -> None:
        self._export_jobs.append((input_file_path, output_file_or_dir_path))

    def export(self) -> None:

        file_args: List[str] = []

        for export_job in self._export_jobs:
            input_file_path = export_job[0]
            output_file_or_dir_path = export_job[1]

            if output_file_or_dir_path:
                file_args.append(f"{input_file_path}:{output_file_or_dir_path}")
            else:
                file_args.append(str(input_file_path))

        args: List[str] = []

        if which("xvfb-run") is not None:
            logm.info("xvfb available - visual output will be redirected and hidden through xvfb.")
            args.append("xvfb-run")
            args.append("-a")
        else:
            logm.info("xvfb NOT available - unable to hide visual output.")

        args.append("freecad")
        args.append(str(FILE_DIR / "resources/freecad_export_image.py"))
        args.append("--pass")
        args.extend(file_args)

        logm.info("Run freecad with command: %s", " ".join(args))
        completed_process = subprocess.run(args, capture_output=True)

        try:
            for line in completed_process.stdout.decode("utf-8").splitlines():
                logm.info(line)
            logm.info("Export done!")
        except subprocess.CalledProcessError as e:
            logm.error("Export failed!")
            logm.exception(e)

