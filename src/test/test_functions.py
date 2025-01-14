from funcs_worklogger import configure, parse, add_log, combine_log, send_email
import unittest
import subprocess
import csv
import json


class TestFunctions(unittest.TestCase):
    data_csv = subprocess.getoutput(
        ["fake -n 50 'date_this_year, company, user_name, address, pyint, text' -f csv -c timestamp,job,proj,loc,time,message"]
    )
    print(data_csv)
    data_json = subprocess.getoutput(
        ["fake -n 50 'date_this_year, company, user_name, address, pyint, text' -f json -c timestamp,job,proj,loc,time,message"]
    )
    print(data_json)

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
