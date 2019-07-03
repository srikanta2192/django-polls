
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth.decorators import login_required

from quora.decorators import user_is_post_author
from quora.models import Like, Post
from quora.views import current_user
from django.contrib.auth import get_user


class EditPostPageView(generic.View):

    @method_decorator(login_required)
    @method_decorator(user_is_post_author)
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        current_user_details = get_user(request)
        if current_user_details is not None:
            template = 'quora/post/create.html'
            context = {'post': post, 'username': current_user_details.username}
            return render(request, template, context)
        else:
            template = {'post': post, 'username': current_user_details.username}
            messages.info(request, "Login to continue")
            return render(request, template)
