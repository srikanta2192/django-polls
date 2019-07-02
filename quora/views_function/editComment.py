from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import generic

from quora.decorators import user_login_required
from quora.models import Comment, Post
from quora.views import current_user, viewPost


class EditCommentPageView(generic.View):

    @method_decorator(user_login_required)
    def get(self, request, post_id, comment_id):
        post = get_object_or_404(Post, pk=post_id)
        comment = get_object_or_404(Comment, pk=comment_id)
        current_user_details = current_user(request)
        if current_user_details['user'] is not None:
            return render(request, 'quora/editCommentPage.html', {
                'post': post, 'comment': comment, 'username': current_user_details['user']
            })
        else:
            messages.info(request, "Login to continue")
            return render(request, "/quora/login.html")

    @method_decorator(user_login_required)
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
            return render(request, 'quora/error_page.html', context)
