# TODO: Don't forget to strftime the fake dates for my TIME_FORMAT
from src.args_worklogger import parser
from argparse import Namespace
import subprocess
import os
import unittest
import random


TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%Z"
FIELDS = ["timestamp", "job", "proj", "loc", "time", "start", "end", "desc"]


class TestArgs(unittest.TestCase):
    fields = ''
    for x in FIELDS:
        if x == 'start' or x == 'end':
            continue
        fields += f'{x},'
    cmd = f'fake -n {random.randint(50, 100)} date,job,word,word,time,sentence -f json -c ' + fields
    print(cmd)
    data = subprocess.getoutput(cmd)
    print(data)

    def test_argsbase(self):
        _flags = parser.parse_args(
            [
                'not so great company',
                '-p', 'govwork',
                '-loc', 'remote',
                '-t', '1',
                '-s', 'now',
                '-m', 'testing again, does this work'
            ]
        )
        self.assertIsInstance(_flags, Namespace)
        _flagsDict = vars(_flags)
        self.assertIsInstance(_flagsDict, dict)

    def test_argsmerge(self):
        _filetypes = ['csv', 'text', 'json']
        for file in _filetypes:
            _flags = _flags = parser.parse_args(
                [
                    'test_job',
                    'merge', f'{file}',
                    '--delete'
                ]

            )
            print(_flags)
            self.assertIsInstance(_flags, Namespace)
            _flagsDict = vars(_flags)
            self.assertIsInstance(_flagsDict, dict)
            self.assertEqual(True, _flagsDict['delete'])

        for file in _filetypes:
            _flags = parser.parse_args(
                [
                    'test_job',
                    'merge', f'{file}'
                ]
            )
            self.assertIsInstance(_flags, Namespace)
            _flagsDict = vars(_flags)
            self.assertIsInstance(_flagsDict, dict)
            self.assertEqual(False, _flagsDict['delete'])

    def test_argsemail(self):
        pass


if __name__ == '__main__':
    unittest.main()
