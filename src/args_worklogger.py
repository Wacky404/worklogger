#!/opt/homebrew/bin/python3
"""
ARGUMENTS FILE FOR WORKLOGGER
author: Wacky404
email: wacky404@dev.com
"""

from pathlib import Path
import argparse

parser = argparse.ArgumentParser(
    prog='WorkLogger',
    description="Log time efficiently, accurately, and reliably "
                "directly from the terminal you work in.",
)

subparsers = parser.add_subparsers()

parser_email = subparsers.add_parser(
    'email', help='Send an email of your worklog(s)')

parser.add_argument(
    '-c',
    '--configure',
    action='store_true',
    help='check/create directories that will be used in WorkLogger',
)

parser.add_argument(
    '-l',
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
    '-v',
    '--verbose',
    action='store_false',
    help='turn on/off the verboseness of the program when run',
)

parser.add_argument(
    'job',
    action='store',
    help='Add a job for the work done, to be logged with your insertion',
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

# Email Functionality
parser_email.add_argument(
    '-s',
    '--sender',
    action='store',
    help='whom will be sending the email, if email is provided in config this flag does not need to be used'
)

parser_email.add_argument(
    '-r',
    '--recipient',
    required=True,
    action='store',
    help='whom will be recieving the email'
)

parser_email.add_argument(
    '-p',
    '--path',
    nargs='+',
    action='store',
    required=True,
    help='path(s) to file or directory you want to email'
)
