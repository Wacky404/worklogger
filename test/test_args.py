# TODO: Don't forget to strftime the fake dates for my TIME_FORMAT
from src.args_worklogger import parser
from argparse import Namespace
from pprint import pprint
import subprocess
import os
import unittest
import random
import json


TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%Z"
FIELDS = ["timestamp", "job", "proj", "loc", "time", "start", "end", "desc"]


class TestArgs(unittest.TestCase):
    fields = ''
    for x in FIELDS:
        fields += f'{x},'
    cmd = f'fake -n {random.randint(50, 100)} date_time,job,word,word,time,time,time,sentence -f json -c ' + fields
    data = subprocess.getoutput(cmd)
    json_data: dict = {"logs": []}
    for line in data.split('}'):
        if not line:
            continue

        _propjson = line + '}'
        json_data["logs"].append(json.loads(_propjson))

    for log in json_data["logs"]:
        _ts = log["timestamp"].split()
        _tscorrect = ''
        for i, ele in enumerate(_ts):
            if i == 1:
                _tscorrect += 'T'
            _tscorrect += ele
        log["timestamp"] = _tscorrect + 'UTC'

    def test_argsbase(self):
        for log in self.json_data["logs"]:
            _flags = parser.parse_args(
                [
                    f'{log["job"]}',
                    '-p', f'{log["proj"]}',
                    '-loc', f'{log["loc"]}',
                    '-t', f'{log["time"]}',
                    '-s', f'{log["start"]}',
                    '-m', f'{log["desc"]}'
                ]
            )
            self.assertIsInstance(_flags, Namespace)
            _flagsDict = vars(_flags)
            self.assertIsInstance(_flagsDict, dict)

    def test_argsmerge(self):
        _filetypes = ['csv', 'text', 'json']
        for file in _filetypes:
            _flags = parser.parse_args(
                [
                    'test_job',
                    'merge', f'{file}',
                    '--delete'
                ]

            )
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
