import unittest
import os
from reader import read_csv_files

class TestReader(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = "data"

    def test_read_csv_files(self):
        csv_data = read_csv_files(self.test_data_dir)

        self.assertIn("sample1.csv", csv_data)
        self.assertIn("sample2.csv", csv_data)

        self.assertGreater(len(csv_data["sample1.csv"]), 1)
        self.assertGreater(len(csv_data["sample2.csv"]), 1)

        expected_header = ["name", "age", "email"]
        self.assertEqual(csv_data["sample1.csv"][0], expected_header)

    def test_empty_csv_files(self):
        empty_dir = "tests/empty"
        os.makedirs(empty_dir, exist_ok=True)
        csv_data = read_csv_files(empty_dir)
        self.assertEqual(csv_data, {})

if __name__ == "__main__":
    unittest.main()