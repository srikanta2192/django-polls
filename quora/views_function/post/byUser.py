from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.contrib.auth.models import User
from quora.models import Post
from quora.views import current_user


class PostsByUserView(generic.View):

    def get(self, request, username):
        current_user_details = current_user(request)
        user = get_object_or_404(User, username=username)
        latest_post_list = Post.objects.filter(
            user=user).order_by('-created_at')
        template = 'quora/index.html'
        context = {'latest_post_list': latest_post_list,
                   'username': current_user_details['user']}
        return render(request, template, context)