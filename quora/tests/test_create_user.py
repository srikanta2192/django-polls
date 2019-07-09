import pytest
import django
import os
import unittest
os.environ['DJANGO_SETTINGS_MODULE'] = 'myweb.settings'
django.setup()

from django.db import transaction, IntegrityError
from django.test import Client, RequestFactory
from quora.views_function.createUser import CreateUserView
from quora.forms import UserForm
from quora.models import User



class TestCreateUserView:

    def setup(self):
        pass

    def test_post_should_return_200_if_username_is_valid(self):
        client = Client()
        requestFactory = RequestFactory()
        request = requestFactory.post('/quora/user/create/')
        context = {
            "username":"Test_user",
            "password":"Test_password",
            "email":"test@test.com"
        }
        response = client.post('/quora/user/create/', data=context, follow=True)
        user = User.objects.get(username="Test_create_user")

        assert user.username == "Test_user"
        assert response.status_code == 200


