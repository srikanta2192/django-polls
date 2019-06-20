from django.core.exceptions import PermissionDenied
from quora.models import Post
import pdb
def user_is_post_author(function):
    def wrap(request, *args, **kwargs):
        pdb.set_trace()
        post = Post.objects.get(pk=kwargs['post_id'])
        if post.user.user_name == request.session['user']:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap