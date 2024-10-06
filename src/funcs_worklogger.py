from utils.log_util import logger
from utils import paths_util as pu

import os.path as osp
import os
from datetime import timezone
import datetime
import csv


def configure(dir_list=None):
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


def arg_convert(arguments: dict):
    args: dict = {}
    for key, val in arguments.items():
        args[key] = val

    return args


def parse(filepath=None):
    filename, ext = osp.splitext(osp.basename(filepath))
    logger.debug(f"Parsed: {filename}, {ext}")
    if ext == '.txt':
        with open(filepath, 'r') as fd:
            lines = [line.rstrip() for line in fd]

        return lines
    elif ext == '.csv':
        lines = []
        with open(filepath, 'r') as fd:
            csv_reader = csv.reader(fd, delimiter=',')
            for row in csv_reader:
                lines.append(' '.join(row))

            return lines
    # TODO: Make the parser for json, once I figure out json structure
    elif ext == '.json':
        pass


def add_log(file_format=None, proj_settings=None, savepath=None, backuppath=None, **kwargs):
    dt = datetime.datetime.now(timezone.utc)
    log_str = f"{dt.strftime("%Y-%m-%dT%H:%M:%S%Z")} "
    job_upper = str(kwargs['job']).upper()

    if file_format != None:
        chosen_job = osp.join(savepath, f"{job_upper}{file_format}")
    else:
        chosen_job = osp.join(savepath, f"{job_upper}.txt")

    parsed_file = parse(chosen_job)

    last_entry = str(parsed_file[-1]).split(' ')
    flag_start = False
    flag_end = False
    for param in last_entry:
        param_split = param.split(':')
        var, val = param_split[0], param_split[1] if len(
            param_split) == 2 else None
        if var == 'start':
            flag_start = True
        if var == 'end':
            flag_end = True

    if flag_start and not flag_end and kwargs['end'] == None:
        print(
            f"Your most recent worklog for {str(kwargs['job'])} has no end time.")
        while True:
            add_endtime = input(
                "Do you want to add an end time for the last entry? (Y/n) ")
            if add_endtime == 'Y':
                insert_time = input("End Time: ")
                with open(chosen_job, 'a') as fd:
                    if insert_time == 'now':
                        fd.write(
                            f"{log_str}job:{kwargs['job']} end:{dt.strftime("'%H:%M'")}\n")
                    else:
                        fd.write(
                            f"{log_str}job:{kwargs['job']} end:{insert_time}\n")
                break
            elif add_endtime == 'n':
                break

    for key, val in kwargs.items():
        if key == 'time' and val is not None:
            log_str += f"{key}:{val}hrs "
        elif key == 'message' and val is not None:
            log_str += f"{'desc'}:'{val}' "
        elif key == 'proj' and val is not None and proj_settings is not None:
            job_projects: dict[str, str] = proj_settings[str(
                kwargs['job']).upper()]
            if str(val).upper() in job_projects.keys():
                log_str += f"{key}:{job_projects[str(val).upper()]} "
                logger.debug(
                    f"Job: {kwargs['job']}; Projects: {job_projects}")
            else:
                log_str += f"{key}:{val} "
                logger.debug(
                    f"Couldn't get specified projects for {kwargs['job']} in config.")
        elif key == 'start' and val == 'now':
            log_str += f"{key}:{dt.strftime("'%H:%M'")} "
        elif key == 'start' and val is not None:
            log_str += f"{key}:'{val}' "
        elif key == 'end' and val == 'now':
            log_str += f"{key}:{dt.strftime("'%H:%M'")} "
        elif key == 'end' and val is not None:
            log_str += f"{key}:'{val}' "
        elif val is not None and key != 'file_format' and key != 'proj_settings' and key != 'savepath' and key != 'backuppath':
            log_str += f"{key}:{val} "

    for path in [savepath, backuppath]:
        if file_format != None:
            chosen_job = osp.join(path, f"{job_upper}{file_format}")
        else:
            chosen_job = osp.join(path, f"{job_upper}.txt")

        with open(chosen_job, 'a') as fd:
            fd.write(f"{log_str}\n")

    logger.info(f"Written {kwargs['job']} worklog to {path}")
