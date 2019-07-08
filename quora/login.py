from django.views import generic
from django.shortcuts import render, get_object_or_404
from quora.forms import UserForm
from django.http import HttpResponse, HttpResponseRedirect
from quora.models import User2
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user, login


class LoginPageView(generic.View):

    def get(self, request):
        
        template = 'quora/login.html'
        context = {
            'username': None
        }
        return render(request, template, context)

    def post(self, request):
        if request.method == 'POST':
            form = UserForm(request.POST)
            user = authenticate(
                request, username=form.data['username'], password=form.data['password'])
            temp = User.objects.get(username=form.data['username'])
            if user is not None:
                request.session['user'] = user.username
                request.session['user_id'] = user.id
                login(request, user)
                return HttpResponseRedirect('/quora/')
            else:
                messages.info(
                    request, 'Incorrect login details')
                return HttpResponseRedirect('/quora/loginpage')
        else:
            form = UserForm()
