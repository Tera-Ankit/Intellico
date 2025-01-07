import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.sample_app import *

class TestSample_app(unittest.TestCase):

    def test_add(self):
        # Test for add in sample_app
        result = add(6, 9)  # Replace with actual arguments
        self.assertEqual(result, None)  # Replace with actual expected value

    def test_subtract(self):
        # Test for subtract in sample_app
        result = subtract(7, 2)  # Replace with actual arguments
        self.assertEqual(result, None)  # Replace with actual expected value
