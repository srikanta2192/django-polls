from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib import messages


from quora.views import current_user, viewPost
from quora.models import Post, Comment
from quora.decorators import user_login_required


class EditCommentPageView(generic.View):
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


class EditCommentExecutionView(generic.View):
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
            return HttpResponse("something wrong")
