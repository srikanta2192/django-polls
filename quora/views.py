from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic


from .decorators import user_is_post_author
from .forms import PostForm, UserForm
from .models import Comment, Like, Post, User2
from django.contrib.auth import authenticate, get_user, login
from django.contrib.auth.models import User


class IndexView(generic.View):

    def get(self, request):
        latest_post_list = Post.objects.all().order_by('-created_at')[:20]
        user = get_user(request)
        try:
            for p in latest_post_list:
                p.likes = Like.objects.filter(post_id=p.id).count()
                p.comment = Comment.objects.filter(post_id=p.id)

                if user is not None:
                    p.liked_by_session_user = Like.objects.filter(
                        by_id=user.id, post_id=p.id).count()
                    return render(request, 'quora/index.html', {'latest_post_list': latest_post_list,
                                                            'username': user.username})
                else:
                    return render(request, 'quora/index.html', {'latest_post_list': latest_post_list,
                                                                'username': None})

        except Http404:
            return render(request, 'quora/index.html', {'latest_post_list': latest_post_list,
                                                        'username': None})


def userLogout(request):
    try:
        logout(request)
    except KeyError:
        pass
    return HttpResponseRedirect('/quora/')


def viewPost(request, post_id):
    user = get_user(request)
    try:
        post = Post.objects.get(pk=post_id)
        comment = Comment.objects.filter(post_id=post_id)
        return render(request, 'quora/post/view.html', {'post': post, 'comment': comment, 'username': user.username})
    except ObjectDoesNotExist:
        raise Http404


def current_user(request):
    try:
        user = request.session['user']
        user_id = request.session['user_id']
    except KeyError:
        user = None
        user_id = None

    return {'user': user, 'user_id': user_id}
