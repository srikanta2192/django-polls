from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic

from quora.decorators import user_is_post_author, user_login_required
from quora.forms import PostForm, UserForm
from quora.models import Comment, Like, Post, User
from quora.views import current_user


class CreatePostPageView(generic.View):

    @method_decorator(user_login_required)
    def get(self, request):
        current_user_details = current_user(request)
        return render(request, 'quora/createPostPage.html', {'username': current_user_details['user']})


class CreatePostView(generic.View):

    @method_decorator(user_login_required)
    def post(self, request):
        if request.method == 'POST':
            form = PostForm(request.POST)
        try:
            username = request.session['user']
            if form.is_valid():
                new_post = Post.objects.create(
                    created_at=timezone.now(),
                    content=form.data['content'],
                    likes=0,
                    title=form.data['title'],
                    user=get_object_or_404(User, name=username)
                )
                messages.success(request, "Post is created successfully")
                return HttpResponseRedirect('/quora/')
            else:
                form = PostForm()

        except KeyError:
            messages.info(request, "Login to create a post")
            return render(request, 'quora/login.html')
