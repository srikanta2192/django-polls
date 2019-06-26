from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.utils import timezone
from django.db import IntegrityError
from django.views import generic
from .decorators import user_is_post_author, user_login_required
from .models import Post, User, Like
from .forms import PostForm, UserForm

import pdb

@user_login_required
def commentPage(request, post_id):
    return HttpResponse(post_id)

@user_login_required
def createPost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
    try:
        username = request.session['user']
        if form.is_valid():
            new_post = Post.objects.create(
                post_created_at=timezone.now(),
                post_content=form.data['post_content'],
                post_likes=0,
                title=form.data['title'],
                user=get_object_or_404(User, name=username)
            )
            return HttpResponseRedirect('/quora/')
        else:
            form = PostForm()

    except KeyError:
        return render(request, 'quora/error_page.html', {
            'message': 'Login to create a post please'
        })


@user_login_required
def createPostPage(request):
    return render(request, 'quora/createPostPage.html')


def createUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        try:
            if form.is_valid():
                form.clean_message()
                new_user = User.objects.create(
                    created_at=timezone.now(),
                    name=form.data['username'],
                    password=form.data['password'],
                )
                request.session['user'] = new_user.name
                return HttpResponse('User created successfully')
        except IntegrityError as e:
            return HttpResponse("Username exists! Username should be unique")
        except KeyError:
            return HttpResponse("Login to create a post please")

    else:
        form = PostForm()


@user_login_required
@user_is_post_author
def editPostPage(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'quora/createPostPage.html', {'post': post})


@user_login_required
@user_is_post_author
def editPostSave(request, post_id):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = get_object_or_404(Post, pk=post_id)
            post.title = form.data['title']
            post.post_content = form.data['post_content']
            post.save()
            return HttpResponseRedirect("/quora/{}".format(post_id))
        else:
            form = PostForm()


def index(request):
    latest_post_list = Post.objects.all().order_by('-created_at')[:7]
    for p in latest_post_list:
        p.likes = Like.objects.filter(post_id=p.id).count()

    try:
        user = request.session['user']
        user_id = request.session['user_id']

        for p in latest_post_list:
            p.liked_by_session_user = Like.objects.filter(
                liked_by_id=user_id, post_id=p.id).count() > 0
    except KeyError:
        user = None
    return render(request, 'quora/index.html', {'latest_post_list': latest_post_list,
                                                'username': user})


@user_login_required
def like(request, post_id, username):

    post = get_object_or_404(Post, pk=post_id)
    user = get_object_or_404(User, name=username)

    if Like.objects.filter(
            liked_by_id=user.id, post_id=post_id).count() > 0:
        Like.objects.filter(
            liked_by_id=user.id, post_id=post_id).delete()

    else:
        like = Like.objects.create(post=post, liked_by=user)

    return render(request, 'quora/viewPost.html', {'post': post})


def loginPage(request):
    return render(request, 'quora/login.html')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('quora:index')
    template_name = 'quora/signup.html'


def userLogin(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        user = authenticate(
            username=form.data['username'], password=form.data['password'])
        if user is not None:
            print('correct details')
            login(request, user)
            request.session['user'] = user.username
            request.session['user_id'] = user.id
            return HttpResponseRedirect('/quora/')
        else:
            print('incorrect details')
            return HttpResponse("incorrect details")


def userLogout(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    return HttpResponseRedirect('/quora/')


def user_list(request):
    user_list = User.objects.order_by('-user_created_at')
    output = (', ').join([u.name for u in user_list])

    return HttpResponse(output)


def userPosts(request, username):
    user = User.objects.get(name=username)
    post_list_by_user = Post.objects.filter(user=user)
    return render(request, 'quora/userPosts.html', {'post_list_by_user': post_list_by_user})


def viewPost(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        print(post.id)
        return render(request, 'quora/viewPost.html', {'post': post})
    except ObjectDoesNotExist:
        return HttpResponse("Post does not exist")


# class IndexView(generic.View):
#     template_name = 'quora/index.html'
#     context_object_name = 'latest_post_list'

#     def get_queryset(self):
#         return Post.objects.all().order_by('-post_created_at')[:10]
