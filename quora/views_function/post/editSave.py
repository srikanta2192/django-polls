from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import generic

from quora.decorators import user_is_post_author, user_login_required
from quora.forms import PostForm
from quora.models import Post


class EditPostSaveView(generic.View):
    @method_decorator(user_login_required)
    @method_decorator(user_is_post_author)
    def post(self, request, post_id):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = get_object_or_404(Post, pk=post_id)
                post.title = form.data['title']
                post.content = form.data['content']
                post.save()
                return HttpResponseRedirect("/quora/{}".format(post_id))
            else:
                form = PostForm()
