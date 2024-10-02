from pathlib import Path
from utils.log_util import logger, setup_logging

from args_worklogger import parser
from utils import paths_util as pu
import logging

import os.path as osp
import os
import sys
import json
from datetime import timezone
import datetime

SAVEPATH: Path | str
BACKUPPATH: Path | str
CONFIGPATH: Path | str

formats: dict = {
    "TEXT": '.txt',
    "JSON": '.json',
}

# creates a NameSpace of arguments that were made
args = parser.parse_args()


def configure(dir_list: list | None = None) -> None:
    if dir_list is not None:
        for directory in dir_list:
            try:
                os.makedirs(name=directory, exist_ok=True)
                logger.debug(f"Directory {directory} created")

            except FileExistsError as e:
                logger.exception(f"An exception of type {type(e).__name__} occurred. "
                                 f"Details: This is okay, output will save in existing {directory}.")
    else:
        for directory in [pu.output_dir, pu.log_dir]:
            try:
                os.makedirs(name=directory, exist_ok=True)
                logger.debug(f"Directory {directory} created")

            except FileExistsError as e:
                logger.exception(f"An exception of type {type(e).__name__} occurred. "
                                 f"Details: This is okay, output will save in existing {directory}.")


def add_log(job=args.job, proj=args.project, loc=args.location, time=args.time, start=args.start, end=args.end,
            desc=args.message, file_format=None) -> None:
    # TODO: Add in functionality to convert project input arg to key value pair from settings
    func_args = locals()
    dt = datetime.datetime.now(timezone.utc)
    log_str = f"{dt.strftime("%Y-%m-%dT%H:%M:%S%Z")} "
    for key, val in func_args.items():
        if key == 'time' and val is not None:
            log_str += f"{key}:{val}hrs "
        elif key == 'desc' and val is not None:
            log_str += f"{key}:'{val}'"
        elif val is not None and key != 'file_format':
            log_str += f"{key}:{val} "

    job_upper = str(job).upper()
    for path in [SAVEPATH, BACKUPPATH]:
        if file_format != None:
            chosen_job = osp.join(path, f"{job_upper}{file_format}")
        else:
            chosen_job = osp.join(path, f"{job_upper}.txt")

        with open(chosen_job, 'a') as fd:
            fd.write(f"{log_str}\n")

        logger.info(f"Written {func_args['job']} worklog to {path}")


if args.configure:
    configure()
    logger.info("Configuration completed.")
    sys.exit()

numeric_loglevel = getattr(logging, str(args.log).upper())
if isinstance(numeric_loglevel, int):
    setup_logging(numeric_loglevel)
else:
    setup_logging()


dotfile: list | None = None
if osp.exists(osp.join(os.getcwd(), os.pardir)):
    dotfile = list(Path(osp.join(os.getcwd(), os.pardir)).glob(
        '**/*.workloggerconfig.json'))
    if len(dotfile) > 1:
        logger.error(
            f"You have {len(dotfile)} config files, using defaults...")
        dotfile = None
    else:
        logger.debug(f"Using user config file in {str(dotfile[0])}")

settings = None
if dotfile is not None:
    with open(dotfile[0], 'r') as fd:
        try:
            settings = json.load(fd)
        except Exception as e:
            logger.exception(str(e))
            if args.verbose:
                print("There was an error loading your config.")
                print("Using defaults")

if settings is not None:
    SAVEPATH = Path(osp.join(osp.expanduser("~"), settings['savepath']))
    BACKUPPATH = Path(osp.join(osp.expanduser("~"), settings['backuppath']))
    CONFIGPATH = Path(osp.join(osp.expanduser("~"), settings['configpath']))
    numeric_loglevel_settings = getattr(
        logging, str(settings['loglvl']).upper())
    setup_logging(numeric_loglevel_settings)
    dir_list: list = [d for d in [
        SAVEPATH, BACKUPPATH, CONFIGPATH] if not osp.exists(d)]
    if len(dir_list) > 0:
        configure(dir_list=dir_list)


jobs_names = [str(j['name']).upper() for j in settings['jobs']]
try:
    for name in jobs_names:
        filepath = osp.join(SAVEPATH, f"{name}.txt")
        filepath_backup = osp.join(BACKUPPATH, f"{name}.txt")
        if not osp.exists(filepath):
            with open(filepath, 'x'):
                pass
        if not osp.exists(filepath_backup):
            with open(filepath_backup, 'x'):
                pass
except Exception as e:
    logger.exception(str(e))

if settings is not None:
    add_log(file_format=formats[str(settings['fileformat']).upper()])
else:
    add_log()
