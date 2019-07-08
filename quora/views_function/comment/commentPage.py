from django.contrib import messages
from django.contrib.auth import authenticate, get_user, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import generic

from quora.models import Comment, Post


class CommentPageView(LoginRequiredMixin, generic.View):

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

    def post(self, request, post_id):
        user = get_user(request)
        template = 'quora/post/view.html'
        if user is not None:
            if request.method == 'POST':
                content = request.POST['content']
                if len(content) > 0:
                    post = get_object_or_404(Post, pk=post_id)
                    Comment.objects.create(
                        content=content, by=user, post=post)
                    comment = Comment.objects.filter(post_id=post_id)
                else:
                    messages.info(request, "Content cannot be empty")
                    return CommentPageView.get(CommentPageView, post_id)
        else:
            messages.info(request, "Login to create a post")
            return render(request, 'quora/login.html')

        context = {'post': post, 'comment': comment,
                   'username': user.username}

        return render(request, template, context)