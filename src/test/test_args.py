from args_worklogger import parser
from argparse import Namespace
import unittest


class TestArgs(unittest.TestCase):
    def test_argsbase(self):
        _flags = parser.parse_args(
            "'not so great company' -p govwork -loc remote -t 1 -s now -m 'testing again, does this work'"
        )
        self.assertIsInstance(_flags, Namespace)
        _flagsDict = vars(_flags)
        self.assertIsInstance(_flagsDict, dict)

    def test_argsmerge(self):
        _filetypes = ['csv', 'txt', 'json']
        for file in _filetypes:
            _flags = _flags = parser.parse_args(
                f"'test_job' merge {file} --delete"
            )
            print(_flags)
            self.assertIsInstance(_flags, Namespace)
            _flagsDict = vars(_flags)
            self.assertIsInstance(_flagsDict, dict)
            self.assertEqual(True, _flagsDict['delete'])

        _flags = parser.parse_args(
            "'test_job' merge txt"
        )
        self.assertIsInstance(_flags, Namespace)
        _flagsDict = vars(_flags)
        self.assertIsInstance(_flagsDict, dict)
        self.assertEqual(False, _flagsDict['delete'])

    def test_argsemail(self):
        pass


if __name__ == '__main__':
    unittest.main()
