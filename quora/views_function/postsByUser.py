from django.shortcuts import render, get_object_or_404
from quora.views import current_user
from quora.models import User, Post
from django.views import generic


def postsByUser(request, username):
    current_user_details = current_user(request)
    user = get_object_or_404(User, name=username)
    latest_post_list = Post.objects.filter(
        user=user).order_by('-created_at')

    return render(request, 'quora/index.html', {'latest_post_list': latest_post_list,
                                                'username': current_user_details['user']})


class PostsByUserView(generic.View):

    def get(self, request, username):
        current_user_details = current_user(request)
        user = get_object_or_404(User, name=username)
        latest_post_list = Post.objects.filter(
            user=user).order_by('-created_at')

        return render(request, 'quora/index.html', {'latest_post_list': latest_post_list,
                                                'username': current_user_details['user']})
