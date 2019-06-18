from django.db import models

# Create your models here.


class User(models.Model):
    user_name = models.CharField(max_length=200)
    user_created_at = models.DateTimeField('date user created')

    def __str__(self):
        return self.user_name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=200)
    post_content = models.CharField(max_length=400)
    post_created_at = models.DateTimeField('date post created')
    post_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.post_title
