from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from quora.models import Post, User
from django.contrib import messages



def user_is_post_author(function):
    def wrap(request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['post_id'])
        try:
            if post.user.name == request.session['user']:
                return function(request, *args, **kwargs)
            else:
                messages.info(
                    request, "You dont have access to edit that post")
                return HttpResponseRedirect('/quora')
                # raise PermissionDenied
        except KeyError:
            messages.info(request, "You dont have access to edit that post")
            return HttpResponseRedirect('/quora')

            # raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_login_required(function):
    def wrapper(request, *args, **kwargs):
        try:
            user = request.session['user']
            if user is None:
                return HttpResponseRedirect('/quora/loginpage/')
            else:
                return function(request, *args, **kwargs)
        except KeyError:
            return HttpResponseRedirect('/quora/loginpage/')

    return wrapper
