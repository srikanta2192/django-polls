import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'myweb.settings'
django.setup()

from quora.views import IndexView

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
# Create your tests here.


class IndexViewTestCases(TestCase):
   
   def test_get(self):
       view_class = IndexView

       request = RequestFactory().get('quora/') 
       request.username = AnonymousUser()
       response = IndexView.as_view()
       self.assertEqual(response.status_code, 200)