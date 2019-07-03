from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

DEFAULT_POST_ID = 1
DEFAULT_USER_ID = 1
class User2(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField('date user created')
    password = models.CharField(max_length=100, default='password')

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ["password"]
    is_anonymous = False
    is_authenticated= True
    def __str__(self):
        return "@{}".format(self.name)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=DEFAULT_USER_ID)
    title = models.CharField(max_length=200, default="Post")
    content = models.TextField(max_length=400, default="Conetnt")
    created_at = models.DateTimeField('date post created', default=timezone.now())


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=DEFAULT_POST_ID)
    by = models.ForeignKey(User, on_delete=models.CASCADE, default=DEFAULT_USER_ID)

class Comment(models.Model):
    content = models.TextField(max_length=1000, default="")
    by = models.ForeignKey(User, on_delete=models.CASCADE, default=DEFAULT_USER_ID)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=DEFAULT_POST_ID)
