from django.contrib import messages
from django.contrib.auth import authenticate, get_user, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import generic

from quora.models import Comment, Post
from quora.views import current_user


class CommentPageView(generic.View):

    @method_decorator(login_required)
    def get(self, request, post_id):
        template = 'quora/comment/create.html'
        post = get_object_or_404(Post, pk=post_id)
        user = get_user(request)
        if user is not None:
            context = {
                'post': post,
                'username': user.username
            }
            return render(request, template, context)
        else:
            messages.info(request, "Please login to continue")
            return render(request, 'quora/login.html')
