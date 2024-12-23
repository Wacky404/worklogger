#!/opt/homebrew/bin/python3

"""
IMPLEMENTATION FILE FOR WORKLOGGER
author: Wacky404
email: wacky404@dev.com
"""

from log_util_worklogger import logger
from datetime import timezone, datetime
from pathlib import Path
import paths_util_worklogger as pu
import os.path as osp
import csv
import os


TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


def _prep_write(format, s_log, p_settings, _dt, k_args):
    dt = _dt
    if format == '.txt' or format == None:
        for key, val in k_args.items():
            if key == 'job' and val is not None:
                s_log += f"{key}:'{val}'"
            elif key == 'time' and val is not None:
                s_log += f"{key}:{val}hrs "
            elif key == 'message' and val is not None:
                s_log += f"{'desc'}:'{val}' "
            elif key == 'proj' and val is not None and p_settings is not None:
                job_projects = p_settings[str(k_args['job']).upper()]
                if str(val).upper() in job_projects.keys():
                    s_log += f"{key}:{job_projects[str(val).upper()]} "
                    logger.debug(
                        f"Job: {k_args['job']}; Projects: {job_projects}")
                else:
                    s_log += f"{key}:{val} "
                    logger.debug(
                        f"Couldn't get specified projects for {k_args['job']} in config.")
            elif key == 'start' and val == 'now':
                s_log += f"{key}:{dt.strftime("'%H:%M'")} "
            elif key == 'start' and val is not None:
                s_log += f"{key}:'{val}' "
            elif key == 'end' and val == 'now':
                s_log += f"{key}:{dt.strftime("'%H:%M'")} "
            elif key == 'end' and val is not None:
                s_log += f"{key}:'{val}' "
            elif val is not None:
                s_log += f"{key}:{val} "

        return s_log, None, None

    elif format == '.csv':
        cp_kwargs = {
            'timestamp': f"{dt.strftime(TIME_FORMAT)}"
        }
        for key, val in k_args.items():
            if key == 'message':
                cp_kwargs['desc'] = val
                continue
            elif key == 'proj' and val is not None and p_settings is not None:
                job_projects = p_settings[str(
                    k_args['job']).upper()]
                if str(val).upper() in job_projects.keys():
                    cp_kwargs[key] = job_projects[str(val).upper()]
                    logger.debug(
                        f"Job: {k_args['job']}; Projects: {job_projects}")
                else:
                    logger.debug(
                        f"Couldn't get specified projects for {k_args['job']} in config.")
                continue
            elif key == 'start' and val == 'now':
                cp_kwargs['start'] = f"{dt.strftime("'%H:%M'")}"
                continue
            elif key == 'end' and val == 'now':
                cp_kwargs['end'] = f"{dt.strftime("'%H:%M'")}"
                continue

            cp_kwargs[key] = val

        field_names = [x for x in cp_kwargs.keys()]

        return None, cp_kwargs, field_names

    return None, None, None


def _write_file(p_save, p_backup, format, j_upper, len_file, _cp_kwargs, _log_str, _field_names) -> None:
    for path in [p_save, p_backup]:
        if path is not None:
            if format != None:
                chosen_job = osp.join(path, f"{j_upper}{format}")
            else:
                chosen_job = osp.join(path, f"{j_upper}.txt")
            try:
                if format == '.csv' and len_file == 0 or len_file == None:
                    with open(chosen_job, 'w', newline='\n') as fd:
                        csv_writer = csv.DictWriter(
                            fd, fieldnames=_field_names)
                        csv_writer.writeheader()
                        for _kwarg in _cp_kwargs:
                            csv_writer.writerow(_kwarg)
                elif format == '.csv' and len_file >= 1:
                    with open(chosen_job, 'a', newline='\n') as fd:
                        csv_writer = csv.DictWriter(
                            fd, fieldnames=_field_names)
                        for _kwarg in _cp_kwargs:
                            csv_writer.writerow(_kwarg)
                else:
                    with open(chosen_job, 'a') as fd:
                        for _log in _log_str:
                            fd.write(f"{_log}\n")
            except PermissionError as e:
                logger.exception(str(e))

            logger.info(f"Written {j_upper} worklog(s) to {path}")


def configure(dir_list=None):
    if dir_list is not None:
        for directory in dir_list:
            try:
                os.makedirs(name=directory, exist_ok=True)
            except FileExistsError as e:
                print(f"An exception of type {type(e).__name__} occurred. "
                      f"Details: This is okay, output will save in existing {directory}.")

    else:
        for directory in [pu.output_dir, pu.log_dir]:
            try:
                os.makedirs(name=directory, exist_ok=True)
            except FileExistsError as e:
                print(f"An exception of type {type(e).__name__} occurred. "
                      f"Details: This is okay, output will save in existing {directory}.")


def parse(filepath):
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
                    elif key == 'job':
                        csv_log += f"{key}:'{val}' "
                    elif val:
                        csv_log += f"{key}:{val} "

                lines.append(csv_log)

            return lines
    # TODO: Make the parser for json, once I figure out json structure
    elif ext == '.json':
        pass


def add_log(file_format=None, proj_settings=None, savepath=None, backuppath=None, **kwargs):
    dt = datetime.datetime.now(timezone.utc)
    log_str = f"{dt.strftime(TIME_FORMAT)} "
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
                        if insert_time.lower() == 'now':
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
                                {'timestamp': f"{dt.strftime(TIME_FORMAT)}", 'job': kwargs['job'], 'end': f"{dt.strftime("'%H:%M'")}"})
                        else:
                            csv_writer.writerow(
                                {'timestamp': f"{dt.strftime(TIME_FORMAT)}", 'job': kwargs['job'], 'end': f"{insert_time}"})
                break

            elif add_endtime == 'n':
                break

    log_str, cp_kwargs, field_names = _prep_write(format=file_format, s_log=log_str,
                                                  p_settings=proj_settings, _dt=dt)
    _write_file(p_save=savepath, p_backup=backuppath, format=file_format, j_upper=job_upper, len_file=len(parsed_file),
                _cp_kwargs=[cp_kwargs], _log_str=[log_str], _field_names=field_names)


def combine_log(target_job, specified_ext, target_extension=None, savepath=None, backuppath=None, delete=False):
    if target_job is None:
        logger.info('You must specify a job to run combine_log()')
        return None

    buffer = []
    # changed this from iterating over both dirs; thinking of limiting to one
    if osp.exists(savepath):
        files = list(Path(savepath).glob(f'**/{target_job.upper()}.**'))
        logger.debug(f"Found file(s): {files}")
        if len(files) < 2:
            logger.exception(
                f'combine_log() reqs 2 or more files. Found less than 2 of {target_job.upper()}.*')
            return None

        for file in files:
            buffer.extend(parse(file))

        for index, line in enumerate(buffer):
            buffer[index] = [index, line]

        for content in buffer:
            _entry = content[1].split(' ')
            buffer[content[0]].append(_entry[0])

        try:
            buffer.sort(key=lambda x: datetime.strptime(
                x[2], TIME_FORMAT))
        except ValueError as e:
            logger.exception(f"An exception of type {type(e).__name__} occurred. "
                             f"Details: {str(e)}")
            return None

        csv_logs = []
        if specified_ext == '.csv':
            for log in buffer:
                _log = {}
                split_log = log[1].split(' ')
                for index, param in enumerate(split_log):
                    if index == 0:
                        _log['timestamp'] = param
                        continue

                    split_param = param.split(':')
                    var, val = split_param[0], split_param[1] if len(
                        split_param) == 2 else None
                    if val is not None:
                        _log[var] = val

                csv_logs.append(_log)

        _write_file(p_save=savepath, p_backup=None, format=specified_ext, j_upper=target_job.upper(),
                    len_file=None, _cp_kwargs=csv_logs, _log_str=[x[1] for x in buffer],
                    _field_names=['timestamp', 'job', 'proj', 'loc', 'time', 'start', 'end', 'desc'])

        if delete:
            for file in files:
                if file.suffix != specified_ext:
                    os.remove(file)


def send_email(sender=None, to=None, subject=None, files=None):
    pass
