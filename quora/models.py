from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=200, unique=True)
    user_created_at = models.DateTimeField('date user created')
    password = models.CharField(max_length=100, default='password')


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=200)
    post_content = models.CharField(max_length=400)
    post_created_at = models.DateTimeField('date post created')
    post_likes = models.IntegerField(default=0)

    def recently_created_post(self):
        return Post.objects.all().order_by('-post_created_at')[:5]
