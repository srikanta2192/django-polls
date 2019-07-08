from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.contrib import messages


from quora.models import Like, Post
from quora.views import IndexView


class LikeView(LoginRequiredMixin, generic.View):

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        user = get_user(request)
        if user is not None:
            if Like.objects.filter(
                    by_id=user.id, post_id=post_id).count() > 0:
                Like.objects.filter(
                    by_id=user.id, post_id=post_id).delete()
            else:
                Like.objects.create(post=post, by=user)
            return IndexView.get(IndexView, request)
        else:
            template = "/quora/login.html"
            messages.info(request, "Login to continue")
            return render(request, template)
