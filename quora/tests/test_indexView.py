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
from django.test import Client



class TestIndexView:

    def test_get_api_helper_should_return_latest_list_with_username_in_context_if_user_passed(self):
        user = User.objects.create_user(username="test_index_view_user",
                                        email="test@testemail.com")
        user.set_password("test_password")                                        
        
        post_list = Post.objects.all().order_by('-created_at')[:20]
        context = IndexView.get_api_helper(self,user=user)
        assert context['latest_post_list'].count() == post_list.count()
        assert context['username'] == user.username
        user.delete()

    def test_get_api_helper_should_return_latest_list_with_None_username_if_user_is_not_None(self):
        user = User.objects.create_user(username="test_index_view_user",
                                        email="test@testemail.com",
                                        password="test_password")
        post = Post.objects.create(user=user, created_at=timezone.now(
        ), content="test_post_content", title="test_post_title")
        user.delete()        
        user = None
        post_list = Post.objects.all().order_by('-created_at')[:20]
        context = IndexView.get_api_helper(self,user=None)
        assert context['latest_post_list'].count() == post_list.count()
        assert context['username'] == None


    def test_viewPost_api_helper_should_return_context_with_post_comment_and_username(self):
        user = User.objects.create_user(username="test_index_view_user",
                                        email="test@testemail.com",
                                        password="test_password")
        post = Post.objects.create(user=user, created_at=timezone.now(
        ), content="test_post_content", title="test_post_title")

        comment = Comment.objects.create(
            by=user, content="test_comment_content", post=post)

        context = viewPost_api_helper(user, post.id)
        test_comment_list = set(comment for comment in context['comment'])

        assert context['post'] == post
        assert context['username'] == user.username
        assert test_comment_list == {comment}
        user.delete()


    def test_viewPost_should_make_the_context_none_if_user_or_post_is_not_found(self):
        context = viewPost_api_helper(None, None)
        assert context == None

    def test_viewPost_return_status_404_if_post_does_not_exist(self):
        client = Client()
        response = client.get('/quora/%d/' % (11231))
        assert response.status_code == 404

        