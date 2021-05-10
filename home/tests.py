from home.models import Complaint
from django.http import response
from django.test import TestCase

# Create your tests here.

class URLTests(TestCase):
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        
class TestAppModels(TestCase):
    def test_complaint_name(self):
        name = Complaint.objects.create(name="pawan")
        self.assertEqual(str(name) , "Message from pawan - ")
        
# def setUp(self):
# Its create database for individual test case
# @classmethod
# def setUpTestData(self):
# set up data for whole testcase