from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField('date user created')
    password = models.CharField(max_length=100, default='password')


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=400)
    created_at = models.DateTimeField('date post created')


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    by = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.TextField(max_length=1000, default="")
    by = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
