from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth.decorators import login_required

from quora.decorators import user_is_post_author
from quora.forms import PostForm, UserForm
from quora.models import Comment, Like, Post, User2
from quora.views import current_user


class CreatePostView(generic.View):

    @method_decorator(login_required)
    def get(self, request):
        user = get_user(request)
        template = 'quora/post/create.html',
        context = {'username': user.username}
        return render(request, template, context)

    @method_decorator(login_required)
    def post(self, request):
        if request.method == 'POST':
            form = PostForm(request.POST)
        try:
            username = request.session['user']
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
