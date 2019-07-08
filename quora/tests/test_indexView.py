import pytest
import django
import os
import unittest

os.environ['DJANGO_SETTINGS_MODULE'] = 'myweb.settings'
django.setup()

from quora.models import Post, Comment
from quora.views import IndexView, viewPost, viewPost_api_helper
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase
from django.test import Client



class IndexViewTestCases(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test_user",
                                        email="test@testemail.com",
                                        password="test_password")
        self.post = Post.objects.create(user=self.user, created_at=timezone.now(
        ), content="test_post_content", title="test_post_title")



    def test_get_api_helper_should_return_latest_list_with_username_in_context_if_user_passed(self):
        user = User.objects.create_user(username="test_user2",
                                        email="test@testemail.com")
        user.set_password("test_password")                                        
        post_list = Post.objects.all().order_by('-created_at')[:20]
        context = IndexView.get_api_helper(self,user=user)
        assert context['latest_post_list'].count() == post_list.count()
        assert context['username'] == "test_user2"

    def test_get_api_helper_should_return_latest_list_with_None_username_if_user_is_not_None(self):
        post = Post.objects.create(user=self.user, created_at=timezone.now(
        ), content="test_post_content", title="test_post_title")
        user = None
        post_list = Post.objects.all().order_by('-created_at')[:20]
        context = IndexView.get_api_helper(self,user=None)
        assert context['latest_post_list'].count() == post_list.count()
        assert context['username'] == None

    def test_viewPost_api_helper_should_return_context_with_post_comment_and_username(self):
        comment = Comment.objects.create(
            by=self.user, content="test_comment_content", post=self.post)

        context = viewPost_api_helper(self.user, self.post.id)
        test_comment_list = set(comment for comment in context['comment'])

        assert context['post'] == self.post
        assert context['username'] == self.user.username
        assert test_comment_list == {comment}

    def test_viewPost_should_make_the_context_none_if_user_or_post_is_not_found(self):
        context = viewPost_api_helper(None, None)
        assert context == None

    def test_viewPost_return_status_200_if_post_exists(self):
        response = self.client.get(('/quora/{}/').format(self.post.id))
        assert response.status_code == 200

    def test_viewPost_return_status_404_if_post_does_not_exist(self):
        response = self.client.get('/quora/%d/' % (11231))
        assert response.status_code == 404

        