import pytest
import django
import os
import unittest
os.environ['DJANGO_SETTINGS_MODULE'] = 'myweb.settings'
django.setup()

from quora.models import Post
from quora.views_function.post.create import CreatePostView
from quora.forms import PostForm
from django.contrib.auth import login
from django.contrib.auth import get_user
from django.test import TestCase
from django.utils import timezone
from django.test.client import RequestFactory
from django.test import Client
from django.http import Http404, HttpRequest
from django.test import RequestFactory
from django.contrib.auth.models import User
from importlib import import_module



class CreatePostViewTestCases(TestCase):

    def setup(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test_user",
                                             email="test@testemail.com",
                                             password="test_password")

    def test_get_should_return_response_with_status_code_302_if_there_is_not_session(self):
        client = Client()
        response = client.get('/quora/post/create/')

        assert response.status_code == 302

    def test_get_should_return_response_with_status_code_200_if_session_exists(self):
        user = User.objects.create_user(username="test_user",
                                        email="test@testemail.com")
        client = Client()
        client.login(username=user.username, password="test_password")
        response = client.get('/quora/post/create/', follow=True)
        assert response.status_code == 200


    def test_get_should_return_response_with_status_code_200_if_there_is_an_existing_session(self):

        user = User.objects.create_user(username="test_user",
                                        email="test@testemail.com"
                                        )
        user.set_password("test_password")
        client = Client()
        form = PostForm()
        form.data['content'] = "Test_post_content"
        form.data['title'] = "Test_post_title"
        content = {
            'content': "Test_post_content",
            'title': "Test_post_title"
        }
        request = HttpRequest()
        request.POST['content'] = "test_content"
        request.POST['title'] = "test_title"
        request.method = 'POST'
        client.login(username=user.username, password="test_password")
        response = client.post('/quora/post/create/save/', data=content, content_type="application/x-www-form-urlencoded",
                               follow=True)
        post = Post.objects.filter(title="Test_post_title")
        assert post is not None                               
        assert response.status_code == 200
