import os
import unittest
from app import app
from app.views import *
from datetime import datetime

# http://tech.waynesimmerson.ca/Article/learn-test-driven-development-flask-part-2
class ViewsTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

        self.corr_year = datetime.now().year-10
        self.corr_month = 6
        self.corr_day = 24
        self.incorrect_month = 30
        self.incorrect_day = 60

    def send_birth_date_and_age(self, year, month, day, expected_age=90):
        return self.app.post('/', 
                            data=dict(
                                birth_year=year,
                                birth_month=month,
                                birth_day=day,
                                expected_age=expected_age),
                            follow_redirects=True)


    def test_page_not_found(self):
        """Pages which dont exist should be directed to a 404 page"""
        rv = self.app.get('/a-page-which-doesnt-exist')
        self.assertEqual(rv.status_code, 404)   

    def test_empty_year(self):
        rv = self.send_birth_date_and_age(year=None, month=self.corr_month, day=self.corr_day)
        self.assertTrue(b"Year of birth is required field" in rv.data)
        self.assertFalse(b"Month of birth is required field" in rv.data)
        self.assertFalse(b"Day of birth is required field" in rv.data)
    
    def test_empty_month(self):
        rv = self.send_birth_date_and_age(year=self.corr_year, month=None, day=self.corr_day)
        self.assertFalse(b"Year of birth is required field" in rv.data)
        self.assertTrue(b"Month of birth is required field" in rv.data)
        self.assertFalse(b"Day of birth is required field" in rv.data)

    def test_empty_day(self):
        rv = self.send_birth_date_and_age(year=self.corr_year, month=self.corr_month, day=None)
        self.assertFalse(b"Year of birth is required field" in rv.data)
        self.assertFalse(b"Month of birth is required field" in rv.data)
        self.assertTrue(b"Day of birth is required field" in rv.data)

    def test_impossible_dates(self):
        rv = self.send_birth_date_and_age(year=self.corr_year, month='02', day='30')
        self.assertTrue(b"Incorrect date entered" in rv.data)
        rv = self.send_birth_date_and_age(year=self.corr_year, month=self.corr_month, day=self.incorrect_day)
        self.assertTrue(b"Incorrect date entered" in rv.data)
        rv = self.send_birth_date_and_age(year=self.corr_year, month=self.incorrect_month, day=self.corr_day)
        self.assertTrue(b"Incorrect date entered" in rv.data)
  
    def test_years(self):
        rv = self.send_birth_date_and_age(year=datetime.now().year-110, month=self.corr_month, day=self.corr_day)
        self.assertTrue(b"You can&#39;t be that old!" in rv.data)
        rv = self.send_birth_date_and_age(year=datetime.now().year+100, month=self.corr_month, day=self.corr_day)
        self.assertTrue(b"Are you from future?" in rv.data)  

    def test_expected_age(self):
        rv = self.send_birth_date_and_age(year=self.corr_year, month=self.corr_month, day=self.corr_day, expected_age=-10)
        self.assertTrue(b"Age have to be in range 1-100" in rv.data)
        rv = self.send_birth_date_and_age(year=self.corr_year, month=self.corr_month, day=self.corr_day, expected_age=200)
        self.assertTrue(b"Age have to be in range 1-100" in rv.data)
        rv = self.send_birth_date_and_age(year=self.corr_year, month=self.corr_month, day=self.corr_day, expected_age=80)
        self.assertFalse(b"Age have to be in range 1-100" in rv.data)
        rv = self.send_birth_date_and_age(year=self.corr_year, month=self.corr_month, day=self.corr_day)
        self.assertFalse(b"Age have to be in range 1-100" in rv.data)
   
    def test_group(self):
        self.assertEqual(
                        group([1,2,3,4,5,6,7,8,9,10],1),
                        [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
                        )
        self.assertEqual(
                        group([1,2,3,4,5,6,7,8,9,10],2),
                        [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
                        )
        self.assertEqual(
                        group([1,2,3,4,5,6,7,8,9,10],3),
                        [[1,2,3],[4,5,6],[7,8,9],[10]]
                        )
        self.assertEqual(
                        group([1,2,3,4,5,6,7,8,9,10],0),
                        [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
                        )
        self.assertEqual(
                        group([1,2,3,4,5,6,7,8,9,10],-10),
                        [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
                        )
        # test tuple
        self.assertEqual(
                        group((1,2,3,4,5,6,7,8,9,10),3),
                        [(1,2,3),(4,5,6),(7,8,9),(10,)]
                        )

    def test_shift_month(self):
        self.assertEqual(
                        shift_month(datetime(2000,12,25), 1),
                        datetime(2001,1,25)
                        )
        self.assertEqual(
                        shift_month(datetime(2000,12,25), -1),
                        datetime(2000,11,25)
                        )


if __name__ == '__main__':
    unittest.main()