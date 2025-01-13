#!/opt/homebrew/bin/python3
"""
ARGUMENTS FILE FOR WORKLOGGER
author: Wacky404
email: wacky404@dev.com
"""

from funcs_worklogger import configure
import argparse


class action_configure(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        return super().__init__(option_strings, dest, nargs=0, default=argparse.SUPPRESS, **kwargs)

    def __call__(self, parser, namespace, values, option_strings, **kwargs):
        configure(dir_list=None)
        parser.exit()


parser = argparse.ArgumentParser(
    prog='WorkLogger',
    description="Log time efficiently, accurately, and reliably "
                "directly from the terminal you work in.",
)

parser.add_argument(
    '--configure',
    action=action_configure,
    help='check/create, log & output, directories that will be used in WorkLogger',
)

parser.add_argument(
    '--log',
    action='store',
    default='INFO',  # NOTSET=0, DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50
    help='DEBUG: Detailed information for diagnosing problems | '
         'INFO: Confirmation that things are working | '
         'WARNING: Indication that something unexpected happened. Program still running | '
         'ERROR: Not able to perform some function of the program | '
         'CRITICAL: Serious error, program may be unable to continue running',
)

parser.add_argument(
    '--verbose',
    action='store_true',
    help='Turn on a verbose program when run',
)

parser.add_argument(
    '--version',
    action='version',
    version='%(prog)s 1.0'
)


parser.add_argument(
    'job',
    action='store',
    help='(required)Add a job for the work done, to be logged with your insertion, merged, or emailed',
)

parser.add_argument(
    '-p',
    '--project',
    action='store',
    help='Add a project to for the work done, if in your config uses the value of the key inplace.',
)

parser.add_argument(
    '-loc',
    '--location',
    action='store',
    help='Add a location for the work done, to be logged with your insertion',
)

parser.add_argument(
    '-t',
    '--time',
    action='store',
    default=0,
    help='Recorded in the unit of hours. Example: 0.5 is 30 minutes, recorded as 0.5hrs'
)

parser.add_argument(
    '-s',
    '--start',
    action='store',
    help='Add a start time for the work done, to be logged with your insertion. Use <now> for current time',
)

parser.add_argument(
    '-e',
    '--end',
    action='store',
    help='Add a end time for the work done, to be logged with your insertion. Use <now> for current time',
)

parser.add_argument(
    '-m',
    '--message',
    action='store',
    help='Add a message to accompany your worklog entry'
)

subparsers = parser.add_subparsers(help='subcommand help')

parser_merge = subparsers.add_parser(
    'merge',
    help='Merge Records of a job and specified file extension'
)

# Merge Functionality
parser_merge.add_argument(
    'extension',
    action='store',
    choices=['csv', 'text', 'json'],
    help='(Required)Output file type, as a result of merge. Default is csv'
)

parser_merge.add_argument(
    '--delete',
    action='store_true',
    default=False,
    help='Delete the old individual files that will get merged into one file'
)

parser_email = subparsers.add_parser(
    'email', help='Send an email of your worklog(s)')

# Email Functionality
parser_email.add_argument(
    '-s',
    '--sender',
    action='store',
    help='Whom will be sending the email, if email is provided in config this flag does not need to be used'
)

parser_email.add_argument(
    '-r',
    '--recipient',
    required=True,
    action='store',
    help='(required) Whom will be recieving the email'
)

parser_email.add_argument(
    '-p',
    '--path',
    nargs='+',
    action='store',
    required=True,
    help='Path(s) to file or directory you want to email'
)
