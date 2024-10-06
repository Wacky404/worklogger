"""
INTERFACE FILE FOR WORKLOGGER
author: Wacky404
email: wacky404@dev.com
"""

from argparse import Namespace
from pathlib import Path


def configure(dir_list: list | None) -> None:
    """

    """
    ...


def add_log(file_format: str | None, proj_settings: dict[str, dict] | None, savepath: Path | str, backuppath: Path | str, **kwargs) -> None:
    """

    """
    ...


def arg_convert(arguments: Namespace) -> dict:
    """

    """
    ...


def parse(filepath: Path | str) -> list:
    """

    """
    ...
