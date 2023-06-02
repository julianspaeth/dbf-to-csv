import os
import unittest
import pandas as pd
from helper import get_dbf_files, convert_to_df, write_csv
import sys


class TestDBF(unittest.TestCase):
    path = "examples"
    python_version = sys.version
    print("Python version:", python_version)

    def test_get(self):

        files = get_dbf_files(self.path)
        self.assertTrue(len(files) > 0)
        for file in files:
            self.assertEqual(file.endswith(".dbf"), True)

    def test_convert(self):
        self.files = get_dbf_files(self.path)
        self.assertTrue(len(self.files) > 0)
        for file in self.files:
            df = convert_to_df(file)
            self.assertTrue(type(df) == pd.DataFrame)

    def test_csv(self):
        self.files = get_dbf_files(self.path)
        self.assertTrue(len(self.files) > 0)
        for file in self.files:
            df = convert_to_df(file)
            write_csv(df, f'{os.path.splitext(file)[0]}.csv')
            self.assertTrue(os.path.exists(f'{os.path.splitext(file)[0]}.csv'))


if __name__ == '__main__':
    unittest.main()