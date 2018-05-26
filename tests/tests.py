#!/usr/bin/python3
"""Unittest for geru web challenge([..])
"""
import unittest
max_integer = __import__("app").max_integer


class TestMaxInteger(unittest.TestCase):

#    def test_int_in_list(self):
#        self.assertEqual(max_integer([1, 2, 3, 4]), 4)


class ExpectedFailureCase(unittest.TestCase):

#    @unittest.expectedFailure
#    def test_string_in_list(self):
#        self.assertEqual(max_integer(["Hello", 2, 3, 4]), 4)



if __name__ == '__main__':
    unittest.main()
