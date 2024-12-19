"""
INTERFACE FILE FOR WORKLOGGER
author: Wacky404
email: wacky404@dev.com
"""

from argparse import Namespace
from pathlib import Path
from typing import Optional


def configure(dir_list: Optional[list]) -> None:
    """

    """
    ...


def add_log(file_format: Optional[str], proj_settings: Optional[dict[str, dict]], savepath: Optional[Path], backuppath: Optional[Path], **kwargs) -> None:
    # small bug in function that is missing an unchecked log start time
    """

    """
    ...


def combine_log(specified_ext: str, target_file: Path, target_extension: Optional[str],
                savepath: Optional[Path], backuppath: Optional[Path], delete: bool = False, **kwargs) -> None:
    """
    Combine logs of different file types into one file of a specified type.

    """
    ...


def parse(filepath: Optional[Path]) -> list:
    # add json parsing, eventually
    """

    """
    ...


def send_email(sender: str, to: str, subject: str, files: list[str | Path]) -> None:
    """

    """
    ...
