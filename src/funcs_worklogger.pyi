"""
INTERFACE FILE FOR WORKLOGGER
author: Wacky404
email: wacky404@dev.com
"""

from argparse import Namespace
from pathlib import Path
from typing import Optional, Any


def _prep_write(format: str, s_log: str, p_settings: dict, _dt, k_args: dict) -> tuple[Optional[str], Optional[dict[str, Any]], Optional[list[str]]]:
    """

    """
    ...


def _write_file(p_save: Optional[Path], p_backup: Optional[Path], format: str, j_upper: str, len_file: int, _cp_kwargs: list[dict], _log_str: list[str], _field_names: list[str]) -> None:
    """

    """
    ...


def configure(dir_list: Optional[list]) -> None:
    """

    """
    ...


def add_log(file_format: Optional[str], proj_settings: Optional[dict[str, dict]], savepath: Optional[Path], backuppath: Optional[Path], **kwargs) -> None:
    """

    """
    ...


def combine_log(target_job: str, specified_ext: str, savepath: Optional[Path], backuppath: Optional[Path], delete: bool = False, **kwargs) -> None:
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
