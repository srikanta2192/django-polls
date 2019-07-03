
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth.decorators import login_required

from quora.models import Comment, Post
from quora.views import current_user
from django.contrib.sessions.models import Session
from .commentPage import CommentPageView
from django.contrib.auth import authenticate, get_user, login
from django.contrib.auth.decorators import login_required


class CreateCommentView(generic.View):

    @method_decorator(login_required)
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
