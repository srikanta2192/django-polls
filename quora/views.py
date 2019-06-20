from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.db import IntegrityError
from django.views import generic
from .decorators import user_is_post_author
from .models import Post, User
from .forms import PostForm, UserForm

import pdb


@login_required
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
                post_title=form.data['post_title'],
                user=get_object_or_404(User, user_name=username)
            )
            return HttpResponseRedirect('/quora/')
        else:
            form = PostForm()

    except KeyError:
        return render(request, 'quora/error_page.html', {
            'message': 'Login to create a post please'
        })


@login_required
def createPostPage(request):
    try:
        if request.session['user']:
            return render(request, 'quora/createPostPage.html')
        else:
            return render(request, 'quora/login.html')

    except KeyError:
        return render(request, 'quora/login.html')


def createUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        try:
            if form.is_valid():
                form.clean_message()
                new_user = User.objects.create(
                    user_created_at=timezone.now(),
                    user_name=form.data['username'],
                    password=form.data['password'],
                )
                request.session['user'] = new_user.user_name
                return HttpResponse('User created successfully')
        except IntegrityError as e:
            return HttpResponse("Username exists! Username should be unique")
        except KeyError:
            return HttpResponse("Login to create a post please")

    else:
        form = PostForm()


@login_required
@user_is_post_author
def editPostPage(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    return HttpResponse("hello")


def index(request):
    latest_post_list = Post.objects.all().order_by('-post_created_at')[:5]
    update_post_list = [(p.user for p in latest_post_list)]
    try:
        user = request.session['user']
    except KeyError:
        user = ''
    return render(request, 'quora/index.html', {'latest_post_list': latest_post_list,
                                                'username': user})


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
            request.session['user'] = user.username
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
    output = (', ').join([u.user_name for u in user_list])

    return HttpResponse(output)


# class IndexView(generic.View):
#     template_name = 'quora/index.html'
#     context_object_name = 'latest_post_list'

#     def get_queryset(self):
#         return Post.objects.all().order_by('-post_created_at')[:10]
