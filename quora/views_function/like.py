from django.contrib import messages
from django.contrib.auth import authenticate, get_user, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import generic


from quora.models import Comment, Like, Post, User2
from quora.views import IndexView, current_user


class LikeView(generic.View):

    @method_decorator(login_required)
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        current_user_details = current_user(request)
        user = get_user(request)
        if user is not None:
            if Like.objects.filter(
                    by_id=user.id, post_id=post_id).count() > 0:
                Like.objects.filter(
                    by_id=user.id, post_id=post_id).delete()
            else:
                like = Like.objects.create(post=post, by=user)

            comment = Comment.objects.filter(post_id=post_id)

            return IndexView.get(IndexView, request)
        else:
            template = "/quora/login.html"
            messages.info(request, "Login to continue")
            return render(request, template)
