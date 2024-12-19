#!/opt/homebrew/bin/python3

"""
IMPLEMENTATION FILE FOR WORKLOGGER
author: Wacky404
email: wacky404@dev.com
"""

from pprint import pprint
from log_util_worklogger import logger
from datetime import timezone
import csv
import datetime
import os
import os.path as osp
import paths_util_worklogger as pu


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
            csv_reader = csv.DictReader(fd, delimiter=',')
            for row in csv_reader:
                csv_log = ''
                for key, val in row.items():
                    if key == 'timestamp':
                        csv_log += f"{val} "
                    elif val:
                        csv_log += f"{key}:{val} "

                lines.append(csv_log)

            print(lines)
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
    flag_start = False
    flag_end = False
    if len(parsed_file) > 1:
        last_entry = str(parsed_file[-1]).split(' ')
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
                    if file_format == '.txt':
                        if insert_time == 'now':
                            fd.write(
                                f"{log_str}job:{kwargs['job']} end:{dt.strftime("'%H:%M'")}\n")
                        else:
                            fd.write(
                                f"{log_str}job:{kwargs['job']} end:{insert_time}\n")
                    elif file_format == '.csv':
                        csv_writer = csv.DictWriter(
                            fd, fieldnames=['timestamp'] + [x if x != 'message' else 'desc' for x in kwargs.keys()])
                        if insert_time == 'now':
                            csv_writer.writerow(
                                {'timestamp': f"{dt.strftime("%Y-%m-%dT%H:%M:%S%Z")}", 'job': kwargs['job'], 'end': f"{dt.strftime("'%H:%M'")}"})
                        else:
                            csv_writer.writerow(
                                {'timestamp': f"{dt.strftime("%Y-%m-%dT%H:%M:%S%Z")}", 'job': kwargs['job'], 'end': f"{insert_time}"})
                break

            elif add_endtime == 'n':
                break

    if file_format == '.txt' or file_format == None:
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
            elif val is not None:
                log_str += f"{key}:{val} "
    elif file_format == '.csv':
        cp_kwargs = kwargs
        cp_kwargs = {
            'timestamp': f"{dt.strftime("%Y-%m-%dT%H:%M:%S%Z")}"
        }
        for key, val in kwargs.items():
            if key == 'message':
                cp_kwargs['desc'] = val
                continue
            elif key == 'proj' and val is not None and proj_settings is not None:
                job_projects: dict[str, str] = proj_settings[str(
                    kwargs['job']).upper()]
                if str(val).upper() in job_projects.keys():
                    cp_kwargs[key] = job_projects[str(val).upper()]
                    logger.debug(
                        f"Job: {kwargs['job']}; Projects: {job_projects}")
                else:
                    logger.debug(
                        f"Couldn't get specified projects for {kwargs['job']} in config.")
                continue
            elif key == 'start' and val == 'now':
                cp_kwargs['start'] = f"{dt.strftime("'%H:%M'")}"
                continue
            elif key == 'end' and val == 'now':
                cp_kwargs['end'] = f"{dt.strftime("'%H:%M'")}"
                continue

            cp_kwargs[key] = val

        field_names = [x for x in cp_kwargs.keys()]

    for path in [savepath, backuppath]:
        if file_format != None:
            chosen_job = osp.join(path, f"{job_upper}{file_format}")
        else:
            chosen_job = osp.join(path, f"{job_upper}.txt")
        try:
            if file_format == '.csv' and len(parsed_file) == 0:
                with open(chosen_job, 'w', newline='\n') as fd:
                    csv_writer = csv.DictWriter(fd, fieldnames=field_names)
                    csv_writer.writeheader()
                    csv_writer.writerow(cp_kwargs)
            elif file_format == '.csv' and len(parsed_file) >= 1:
                with open(chosen_job, 'a', newline='\n') as fd:
                    csv_writer = csv.DictWriter(fd, fieldnames=field_names)
                    csv_writer.writerow(cp_kwargs)
            else:
                with open(chosen_job, 'a') as fd:
                    fd.write(f"{log_str}\n")
        except PermissionError as e:
            logger.exception(str(e))

        logger.info(f"Written {kwargs['job']} worklog to {path}")


def combine_log(specified_ext, target_job, target_extension=None, savepath=None, backuppath=None, delete=False):
    # you pick a job then if you want you can choose a specific file type to target for combining into your specified_ext
    # TODO: Finish function stopped just before date sorting; getting a data structure prepped for sorting then transformation
    if target_job is None:
        logger.info('You must specify a job to run combine_log()')
        return None

    for dir in (savepath, backuppath):
        buffer = []
        if osp.exists(dir):
            target_extension = target_extension.strip('.')
            # only thing affected by this blocks if statement
            if target_extension is not None:
                files = list(Path(dir).glob(
                    f'**/{target_job.upper()}.{target_extension}'))
            else:
                files = list(Path(dir).glob(f'**/{target_job.upper()}'))
            logger.debug(f"Found file(s): {files}")
            if len(files) < 2:
                logger.exception(
                    f'combine_log() reqs 2 or more files. Found less than 2 of {target_job.upper()}.{target_extension}')
                return None

            for file in files:
                buffer.append(*parse(file))

            for index, line in enumerate(buffer):
                buffer[index] = [index, line]

            for content in buffer:
                _entry = content[1].split(' ')
                for param in _entry:
                    param_split = param.split(':')
                    var, val = param_split[0], param_split[1] if len(
                        param_split) == 2 else None
                    # need to sort datetimes ... actually easy
                    if var == 'timestamp':
                        buffer[content[0]].append(val)

            buffer.sort(key=lambda x: datetime.strptime(
                x[2], "%Y-%m-%dT%H:%M:%S%Z"))
            pprint(buffer)


def send_email(sender=None, to=None, subject=None, files=None):
    pass
