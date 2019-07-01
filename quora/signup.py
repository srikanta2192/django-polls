from django.views import generic
from django.shortcuts import render
from quora.views import current_user


class SignupView(generic.View):

    def get(self, request):
        user = current_user(request)

        return render(request, 'quora/signup.html', {
            'username': user['user']
        })
