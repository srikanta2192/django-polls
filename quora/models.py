from django.db import models

class User(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="Post")
    content = models.TextField(max_length=400)
    created_at = models.DateTimeField('date post created')


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

class Comment(models.Model):
    content = models.TextField(max_length=1000, default="")
    by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
