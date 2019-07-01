
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import generic

from quora.decorators import user_is_post_author, user_login_required
from quora.models import Like, Post
from quora.views import current_user


class EditPostPageView(generic.View):

    @method_decorator(user_login_required)
    @method_decorator(user_is_post_author)
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        current_user_details = current_user(request)
        if current_user_details['user'] is not None:
            return render(request, 'quora/createPostPage.html', {'post': post, 'username': current_user_details['user']})
        else:
            messages.info(request, "Login to continue")
            return render(request, "/quora/login.html")
