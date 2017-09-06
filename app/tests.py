import os
import unittest
from app import app
import views


class TestCase(unittest.TestCase):

    def test_make_unique_nickname(self):
        assert group([1,2,3,4,5,6,7,8,9,10],3) == [[1,2,3],[4,5,6],[7,8,9],[10]]


if __name__ == '__main__':
    unittest.main()