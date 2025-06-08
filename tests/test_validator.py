import unittest
from validator import validate_row

class TestValidator(unittest.TestCase):
    def test_valid_row(self):
        row = {"name": "Alice", "age": "30", "email": "alice@example.com"}
        schema = {  "name": "string", "age": "int", "email": "string"}
        valid, errors = validate_row(row, schema)
        self.assertTrue(valid)
        self.assertEqual(errors, [])

    def test_invalid_row(self):
        row = {"name": "Bob", "age": "notanumber", "email": "bob@example.com"}
        schema = { "name": "string", "age": "int", "email": "string"}
        valid, errors = validate_row(row, schema)
        self.assertFalse(valid)
        self.assertTrue("age" in e for e in errors)

if __name__ == "__main__":
    unittest.main()