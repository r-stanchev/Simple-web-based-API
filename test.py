import unittest
from flask import Flask
from app import app, db
from models import Pairs
from flask_testing import TestCase

class BaseTestCase(TestCase):
  """The class is used to perform the base configuration needed for testing"""

  # Configure the database type, username, host, port and database name

  app.config['SQLALCHEMY_DATABASE_URI'] = 'cockroachdb://maxroach@localhost:26257/pairs'

  def create_app(self):
    """Return an instance of that app that will be used for testing"""
    return app

  def setUp(self):
    """Create the table and populate it with test data"""
    db.create_all()
    db.session.add(Pairs(key='John',value='Smith'))
    db.session.add(Pairs(key='Tom',value='Fooler'))
    db.session.add(Pairs(key='Mark',value='Radcliffe'))
    db.session.commit()


  def tearDown(self):
    """Remove all data and drop the table to ensure clean tests"""
    db.session.remove()
    db.drop_all()


class FlaskTestCase(BaseTestCase):
  """This class is used to run the actual tests performed on the application"""


  def test_set_success(self):
    """Tests that the endpoint returns status code 200 when accessed successfully"""

    response = self.client.get('/set',query_string=dict(k=1, v=2))
    self.assertEqual(response.status_code,200)


  def test_get_success_code(self):
    """Tests that the endpoint returns status code 200 when accessed successfully"""

    response = self.client.get('/get',query_string=dict(k='Tom'))
    self.assertEqual(response.status_code,200)\


  def test_get_success_result(self):
    """Tests that the endpoint returns the correct value when accessed successfully"""

    response = self.client.get('/get',query_string=dict(k='Tom'))
    self.assertIn(b'Fooler',response.data)


  def test_get_error_code(self):
    """Tests that the endpoint returns status code 404 when the key does not exist"""

    response = self.client.get('/get',query_string=dict(k='Rado'))
    self.assertEqual(response.status_code,404)


  def test_rm_success_code(self):
    """Tests that the endpoint returns status code 200 when accessed successfully"""

    response = self.client.get('/rm',query_string=dict(k='Mark'))
    self.assertEqual(response.status_code,200)


  def test_rm_error_code(self):
    """Tests that the endpoint returns status code 404 when the key does not exist"""

    response = self.client.get('/rm',query_string=dict(k='Rado'))
    self.assertEqual(response.status_code,404)


  def test_clear_success_code(self):
    """Tests that the endpoint returns status code 200 when accessed successfully"""

    response = self.client.get('/clear')
    self.assertEqual(response.status_code,200)


  def test_is_success_code(self):
    """Tests that the endpoint returns status code 200 when accessed successfully"""

    response = self.client.get('/is',query_string=dict(k='Tom'))
    self.assertEqual(response.status_code,200)


  def test_is_error_code(self):
    """Tests that the endpoint returns status code 404 when the key does not exist"""

    response = self.client.get('/is',query_string=dict(k='Rado'))
    self.assertEqual(response.status_code,404)


  def test_getKeys_success_code(self):
    """Tests that the endpoint returns status code 200 when accessed successfully"""

    response = self.client.get('/getKeys')
    self.assertEqual(response.status_code,200)


  def test_getKeys_success_result(self):
    """Tests that the endpoint returns the correct keys when accessed successfully"""

    response = self.client.get('/getKeys')
    self.assertIn(b'John',response.data)
    self.assertIn(b'Tom',response.data)
    self.assertIn(b'Mark',response.data)


  def test_getValues_success_code(self):
    """Tests that the endpoint returns status code 200 when accessed successfully"""

    response = self.client.get('/getValues')
    self.assertEqual(response.status_code,200)


  def test_getValues_success_result(self):
    """Tests that the endpoint returns the correct values when accessed successfully"""

    response = self.client.get('/getValues')
    self.assertIn(b'Smith',response.data)
    self.assertIn(b'Fooler',response.data)
    self.assertIn(b'Radcliffe',response.data)


  def test_getAll(self):
    """Tests that the endpoint returns status code 200 when accessed successfully"""

    response = self.client.get('/getAll')
    self.assertEqual(response.status_code,200)


  def test_getAll(self):
    """Tests that the endpoint returns the correct pairs when accessed successfully"""

    response = self.client.get('/getAll')
    self.assertIn(b'John',response.data)
    self.assertIn(b'Tom',response.data)
    self.assertIn(b'Mark',response.data)



if __name__ == '__main__':
  unittest.main()