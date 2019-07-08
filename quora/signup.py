from django.views import generic
from django.shortcuts import render


class SignupView(generic.View):

    def get(self, request):
        return render(request, 'quora/signup.html', {
            'username': None
        })
