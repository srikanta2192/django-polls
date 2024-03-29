
from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import generic
from django.http import HttpResponseRedirect

from quora.decorators import user_is_post_author
from quora.models import Post
from quora.forms import PostForm

class EditPostPageView(LoginRequiredMixin, generic.View):

    @method_decorator(user_is_post_author)
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        user = get_user(request)
        if user is not None:
            template = 'quora/post/create.html'
            context = {'post': post, 'username': user.username}
            return render(request, template, context)
        else:
            template = {'post': post,
                        'username': user.username}
            messages.info(request, "Login to continue")
            return render(request, template)

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
