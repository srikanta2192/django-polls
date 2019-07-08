from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.http import Http404

from quora.models import Post

from django.core.exceptions import ObjectDoesNotExist


class PostsByUserView(generic.View):

    def get(self, request, username):

        template = 'quora/index.html'
        context = self.get_api_helper(username)
        if context is not None:
            return render(request, template, context)
        elif context is None:
            raise Http404

    def get_api_helper(self, username):
        try:
            user = get_object_or_404(User, username=username)
            latest_post_list = Post.objects.filter(user=user).order_by('-created_at')
            context = {'latest_post_list': latest_post_list,
                       'username': user.username}
        except Http404:
            context = None

        return context
