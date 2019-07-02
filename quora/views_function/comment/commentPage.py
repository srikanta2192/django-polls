from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import generic

from quora.decorators import user_login_required
from quora.models import Comment, Post, User
from quora.views import current_user


class CommentPageView(generic.View):

    @method_decorator(user_login_required)
    def get(self, request, post_id):
        template = 'quora/comment/create.html'
        post = get_object_or_404(Post, pk=post_id)
        current_user_details = current_user(request)
        if current_user_details['user'] is not None:
            context = {
                'post': post,
                'username': current_user_details['user']
            }
            return render(request, template, context)
        else:
            messages.info(request, "Please login to continue")
            return render(request, 'quora/login.html')
