
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import generic

from quora.decorators import user_login_required
from quora.models import Comment, Post, User
from quora.views import current_user
from django.contrib.sessions.models import Session
from .commentPage import CommentPageView


class CreateCommentView(generic.View):

    @method_decorator(user_login_required)
    def post(self, request, post_id):
        current_user_details = current_user(request)
        if current_user_details['user'] is not None:
            user = get_object_or_404(User, name=current_user_details['user'])
            if request.method == 'POST':
                content = request.POST['content']
                if len(content) > 0:
                    post = get_object_or_404(Post, pk=post_id)
                    Comment.objects.create(
                        content=content,by=user, post=post)
                    comment = Comment.objects.filter(post_id=post_id)
                else:
                    messages.info(request, "Content cannot be empty")
                    return CommentPageView.get(CommentPageView, post_id)
        else:
            messages.info(request, "Login to create a post")
            return render(request, 'quora/login.html')

        return render(request, 'quora/viewPost.html', {'post': post, 'comment': comment, 'username': current_user_details['user']})

