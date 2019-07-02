from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from .decorators import user_is_post_author, user_login_required
from .forms import PostForm, UserForm
from .models import Comment, Like, Post, User


@user_login_required
def commentPage(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    current_user_details = current_user(request)
    if current_user_details['user'] is not None:
        return render(request, 'quora/commentPage.html', {
            'post': post,
            'username': current_user_details['user']
        })
    else:
        messages.info(request, "Please login to continue")
        return render(request, 'quora/login.html')


@user_login_required
def changePasswordPage(request):
    current_user_details = current_user(request)
    if current_user_details['user'] is not None:
        return render(request, 'quora/changePasswordPage.html', {
            'username': current_user_details['user']})
    else:
        messages.info(request, "Please login to continue")
        return render(request, 'quora/login.html')


def changePassword(request):
    current_user_details = current_user(request)
    if current_user_details['user'] is not None:
        if request.method == 'POST':
            user = get_object_or_404(User, name=current_user_details['user'])
            oldPassword = request.POST['oldPassword']
            if oldPassword == user.password:
                newPassword = request.POST['newPassword']
                confirmPassword = request.POST['confirmPassword']
                if newPassword == confirmPassword:
                    user.password = newPassword
                    user.save()
                    messages.success(request, 'Password successfully changed')
                    Session.objects.all().delete()
                    return render(request, 'quora/login.html')
                else:
                    messages.info(
                        request, 'New password and confirm password don\'t match')
                    return render(request, 'quora/changePasswordPage.html', {'username': current_user_details['user']})
            else:
                messages.info(
                    request, 'Password is incorrect')
                return render(request, 'quora/changePasswordPage.html', {'username': current_user_details['user']})
    else:
        messages.info(request, "Please login to continue")
        return render(request, 'quora/login.html')


@user_login_required
def createComment(request, post_id):
    current_user_details = current_user(request)
    if current_user_details['user'] is not None:
        user = get_object_or_404(User, name=current_user_details['user'])
        if request.method == 'POST':
            content = request.POST['content']
            if len(content) > 0:
                post = get_object_or_404(Post, pk=post_id)
                Comment.objects.create(
                    content=content, by=user, post=post)
                comment = Comment.objects.filter(post_id=post_id)
            else:
                messages.info(request, "Content cannot be empty")
                return commentPage(request, post_id)
    else:
        messages.info(request, "Login to create a post")
        return render(request, 'quora/login.html')

    return render(request, 'quora/viewPost.html', {'post': post, 'comment': comment, 'username': current_user_details['user']})


@user_login_required
def createPost(request):
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


@user_login_required
def createPostPage(request):
    current_user_details = current_user(request)
    return render(request, 'quora/createPostPage.html', {'username': current_user_details['user']})


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
                messages.success(request, "User created successfully")
                return HttpResponseRedirect('/quora/')
        except IntegrityError as e:
            messages.info(request,
                          "Username exist! Please try with a different username")
            return HttpResponseRedirect("/quora/signup")
        except KeyError:
            messages.info(request,
                          "Please login")

            return HttpResponseRedirect("/quora/login")

    else:
        form = PostForm()


def current_user(request):
    try:
        user = request.session['user']
        user_id = request.session['user_id']
    except KeyError:
        user = None
        user_id = None

    return {'user': user, 'user_id': user_id}


@user_login_required
def editCommentPage(request, post_id, comment_id):
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


@user_login_required
def editComment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.content = request.POST['content']
        if len(comment.content) > 0:
            comment.save()
            messages.success(request, "Comment posted successfully")
            return viewPost(request, comment.post.id)
        else:
            messages.info(request, "Comment should not be empty")
            return editCommentPage(request, comment.post.id, comment_id)
    else:
        return HttpResponse("something wrong")


@user_login_required
@user_is_post_author
def editPostPage(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    current_user_details = current_user(request)
    if current_user_details['user'] is not None:
        return render(request, 'quora/createPostPage.html', {'post': post, 'username': current_user_details['user']})
    else:
        messages.info(request, "Login to continue")
        return render(request, "/quora/login.html")


@user_login_required
@user_is_post_author
def editPostSave(request, post_id):
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


class IndexView(generic.View):

    def get(self, request):
        latest_post_list = Post.objects.all().order_by('-created_at')[:20]
        current_user_details = current_user(request)
        try:
            user = get_object_or_404(User, name=current_user_details['user'])
            for p in latest_post_list:
                p.likes = Like.objects.filter(post_id=p.id).count()
                p.comment = Comment.objects.filter(post_id=p.id)

                if user is not None:
                    p.liked_by_session_user = Like.objects.filter(
                        by_id=user.id, post_id=p.id).count()
            return render(request, 'quora/index.html', {'latest_post_list': latest_post_list,
                                                        'username': current_user_details['user']})
        except Http404:
            return render(request, 'quora/index.html', {'latest_post_list': latest_post_list,
                                                        'username': None})

@user_login_required
def like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    current_user_details = current_user(request)
    user = get_object_or_404(User, name=current_user_details['user'])
    if current_user_details['user'] is not None:
        if Like.objects.filter(
                by_id=user.id, post_id=post_id).count() > 0:
            Like.objects.filter(
                by_id=user.id, post_id=post_id).delete()
        else:
            like = Like.objects.create(post=post, by=user)

        comment = Comment.objects.filter(post_id=post_id)

        return IndexView.get(IndexView, request)
    else:
        messages.info(request, "Login to continue")
        return render(request, "/quora/login.html")


def loginPage(request):
    return render(request, 'quora/login.html')


def signUp(request):
    user = current_user(request)
    return render(request, 'quora/signup.html', {
        'username': user['user']
    })


def postsByUser(request, username):
    current_user_details = current_user(request)
    user = get_object_or_404(User, name=username)
    latest_post_list = Post.objects.filter(
        user=user).order_by('-created_at')

    return render(request, 'quora/index.html', {'latest_post_list': latest_post_list,
                                                'username': current_user_details['user']})


def userLogin(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        user = get_object_or_404(User, name=form.data['username'])
        if form.data['password'] == user.password:
            request.session['user'] = user.name
            request.session['user_id'] = user.id
            return HttpResponseRedirect('/quora/')
        else:
            messages.info(
                request, 'Incorrect login details')
            return HttpResponseRedirect('/quora/loginpage')
    else:
        form = UserForm()


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


def viewPost(request, post_id):
    current_user_details = current_user(request)
    try:
        post = Post.objects.get(pk=post_id)
        comment = Comment.objects.filter(post_id=post_id)
        return render(request, 'quora/viewPost.html', {'post': post, 'comment': comment, 'username': current_user_details['user']})
    except ObjectDoesNotExist:
        raise Http404