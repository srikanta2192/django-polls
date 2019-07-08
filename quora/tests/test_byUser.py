import pytest
import django
import os
import unittest
os.environ['DJANGO_SETTINGS_MODULE'] = 'myweb.settings'
django.setup()



from django.http import Http404
from django.test import Client
from django.utils import timezone
from django.contrib.auth.models import User
from quora.views_function.post.byUser import PostsByUserView
from django.core.exceptions import ObjectDoesNotExist
from unittest.mock import *
from quora.models import Post, Comment
from django.test import TestCase

class ByUserTestCases(TestCase):

    def setup(self):
        self.client = Client()

    def test_get_api_helper_should_return_post_list_by_specific_user_if_username_is_passed(self):
        p = PostsByUserView()
        user = User.objects.create_user(username="test_user",
                                        email="test@testemail.com",
                                        password="test_password")
        post = Post.objects.create(user=user, created_at=timezone.now(
        ), content="test_post_content", title="test_post_title")

        post2 = Post.objects.create(user=user, created_at=timezone.now(
        ), content="test_post_content", title="test_post_title")

        context = p.get_api_helper(username=user.username)
        test_post_list = set(post for post in context['latest_post_list'])
        compare_post_list = set([post, post2])

        assert test_post_list == compare_post_list

    def test_get_api_helper_should_return_none_if_user_does_not_exist(self):
        p = PostsByUserView()
        context = p.get_api_helper(username=None)
        assert context == None

    def test_det_should_return_404_if_user_does_not_exists(self):
        url=('/quora/test_user/userPosts/')
        
        response = self.client.get(url)
        assert response.status_code == 404
