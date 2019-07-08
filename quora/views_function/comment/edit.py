from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import generic

from quora.models import Comment, Post
from quora.views import viewPost


class EditCommentPageView(generic.View):

    @method_decorator(login_required)
    def get(self, request, post_id, comment_id):
        template = 'quora/comment/edit.html'
        post = get_object_or_404(Post, pk=post_id)
        comment = get_object_or_404(Comment, pk=comment_id)
        user = get_user(request)
        context = {
            'post': post, 'comment': comment, 'username': user.username
        }
        if user is not None:
            return render(request, template, context)
        else:
            messages.info(request, "Login to continue")
            return render(request, "/quora/login.html")

    @method_decorator(login_required)
    def post(self, request, comment_id):
        if request.method == 'POST':
            comment = get_object_or_404(Comment, pk=comment_id)
            comment.content = request.POST['content']
            if len(comment.content) > 0:
                comment.save()
                messages.success(request, "Comment posted successfully")
                return viewPost(request, comment.post.id)
            else:
                messages.info(request, "Comment should not be empty")
                return EditCommentPageView(EditCommentPageView, request, comment.post.id, comment_id)
        else:
            context = {
                'message': 'Something\'s wrong'
            }
            template = 'quora/error_page.html'
            return render(request, template, context)
