from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import generic

from quora.decorators import user_is_post_author
from quora.forms import PostForm
from quora.models import Post


class CreatePostView(LoginRequiredMixin, generic.View):

    def get(self, request):
        user = get_user(request)
        template = 'quora/post/create.html',
        context = {'username': user.username}

        return render(request, template, context)

    def post(self, request):
        if request.method == 'POST':
            form = PostForm(request.POST)
        try:
            if form.is_valid():
                new_post = Post.objects.create(
                    created_at=timezone.now(),
                    content=form.data['content'],
                    title=form.data['title'],
                    user=get_user(request)
                )
                messages.success(request, "Post is created successfully")
                return HttpResponseRedirect('/quora/')
            else:
                form = PostForm()

        except KeyError:
            template = 'quora/login.html'
            messages.info(request, "Login to create a post")
            return render(request, template)
