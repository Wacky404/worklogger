# TODO: ADD in fake text data then start writing tests for functions, want to change some things with the functions first
from src.funcs_worklogger import configure, parse, add_log, combine_log, send_email
from pprint import pprint
import unittest
import subprocess
import csv
import json
import random


TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%Z"
FIELDS = ["timestamp", "job", "proj", "loc", "time", "start", "end", "desc"]


class TestFunctions(unittest.TestCase):
    fields = ''
    for x in FIELDS:
        fields += f'{x},'

    json_cmd = f'fake -n {random.randint(50, 100)} date_time,job,word,word,time,time,time,sentence -f json -c ' + fields
    data = subprocess.getoutput(json_cmd)

    json_data: dict = {"logs": []}
    for line in data.split('}'):
        if not line:
            continue

        _propjson = line + '}'
        json_data["logs"].append(json.loads(_propjson))

    csv_data: list[list] = [[k for k in json_data["logs"][0].keys()]]
    for log in json_data["logs"]:
        _ts = log["timestamp"].split()
        _tscorrect = ''
        for i, ele in enumerate(_ts):
            if i == 1:
                _tscorrect += 'T'
            _tscorrect += ele
        log["timestamp"] = _tscorrect + 'UTC'

        csv_data.append([v for v in log.values()])

    pprint(csv_data)

    def test_configure(self):
        pass

    def test_parse(self):
        pass

    def test_add_log(self):
        pass

    def test_combine_log(self):
        pass

    def test_send_email(self):
        pass


if __name__ == '__main__':
    unittest.main()
