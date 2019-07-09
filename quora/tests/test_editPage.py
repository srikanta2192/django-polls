import pytest
import django
import os
import unittest

os.environ['DJANGO_SETTINGS_MODULE'] = 'myweb.settings'
django.setup()



from quora.models import Post, Comment
from quora.forms import PostForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import Client

class TestEditPostPageView:

    def test_gest_should_return_200_if_user_is_the_post_author(self):
        user = User.objects.create_user(username="test_edit_page_user",
                                        email="test@testemail.com")
        post = Post.objects.create(user=user, created_at=timezone.now(
        ), content="test_post_content", title="test_post_title")

        client = Client()
        client.login(username=user.username, password="test_password")
        response = client.get(
            ("/quora/{}/post/edit/").format(post.id), follow=True)
        assert response.status_code == 200
        user.delete()

    def test_gest_should_return_302_if_user_is_not_the_post_author(self):
        user = User.objects.create_user(username="test_edit_page_user",
                                        email="test@testemail.com")
        user2 = User.objects.create_user(username="test_edit_page_user2",
                                         email="test@testemail.com")
        post = Post.objects.create(user=user, created_at=timezone.now(
        ), content="test_post_content", title="test_post_title")

        client = Client()
        client.login(username=user2.username, password="test_password")
        response = client.get(
            ("/quora/{}/post/edit/").format(post.id))
        assert response.status_code == 302
        user.delete()
        user2.delete()

    def test_post_should_return_200_and_post_should_be_saved_if_user_session_exists(self):
        
        
        user = User.objects.create_user(username="test_edit_page_user",
                                        email="test@testemail.com"
                                        )
        user.set_password("test_password")                                        
        post = Post.objects.create(user=user, created_at=timezone.now(
        ), content="test_post_content", title="test_post_title")
        url = "/quora/{}/post/save/".format(post.id)
        
        user.set_password("test_password")
        client = Client()
        content = {
            'content': "Test_post_content2",
            'title': "Test_post_title2"
        }
        form = PostForm()
        form.data['content'] = "test_post_content"
        form.data['title'] = "test_post_title"

        client.login(username=user.username, password="test_password")
        response = client.post(url, data=form, content_type="application/x-www-form-urlencoded", follow=True
                               )
        assert response.status_code == 200
        user.delete()
