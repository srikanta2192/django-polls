import pytest
import django
import os
import unittest
os.environ['DJANGO_SETTINGS_MODULE'] = 'myweb.settings'
django.setup()


from django.db import transaction, IntegrityError
from django.test import Client
from django.utils import timezone

from quora.views_function.createUser import CreateUserView
from quora.forms import UserForm
from quora.models import User, Post, Comment



class TestCommentPageView:

    def test_get_should_return_response_with_status_code_302_if_there_is_not_session(self):
        client = Client()
        response = client.get('/quora/comment/create/')
        user = User.objects.create_user(username="test_comment_user",
                                             email="test@testemail.com",
                                             password="test_password")
        post = Post.objects.create(user=user, created_at=timezone.now(
        ), content="test_post_content", title="test_post_title")
        
        response = client.get(("/quora/{}/comment/").format(post.id))

        assert response.status_code == 302
        user.delete()

    def test_get_should_return_response_with_status_code_200_if_session_exists(self):
        user = User.objects.create_user(username="test_comment_user",
                                        email="test@testemail.com")
        user.set_password("test_password")
        client = Client()
        post = Post.objects.create(user=user, created_at=timezone.now(
        ), content="test_post_content", title="test_post_title")
        
        client.login(username=user.username, password="test_password")
        response = client.get(("/quora/{}/comment/").format(post.id), follow=True)
        assert response.status_code == 200
        user.delete()

    def test_post_should_save_the_comment_and_return_200_as_status_code(self):
        client = Client()
        user = User.objects.create_user(username="test_comment_user",
                                        email="test@testemail.com")
        user.set_password("test_password")
        post = Post.objects.create(user=user, created_at=timezone.now(
        ), content="test_post_content", title="test_post_title")
        
        context = {
            "content":"Test_comment_content"
        }
        client.login(username="test_comment_user", password="test_password") 
        url = ("/quora/{}/createComment/").format(post.id)
        response = client.post(url, data=context, follow=True)
        assert response.status_code == 200
        user.delete()