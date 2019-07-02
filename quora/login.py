from django.views import generic
from django.shortcuts import render, get_object_or_404
from quora.views import current_user
from quora.forms import UserForm
from django.http import HttpResponse, HttpResponseRedirect
from quora.models import User
from django.contrib import messages

from django.contrib.auth import authenticate, login


class LoginPageView(generic.View):

    def get(self, request):
        user = current_user(request)
        template = 'quora/login.html'
        context = {
            'username': user['user']
        }
        return render(request, template, context)

    def post(self, request):
        if request.method == 'POST':
            form = UserForm(request.POST)
            user = authenticate(
                request, username=form.data['username'], password=form.data['password'])
            print(user)
            user = get_object_or_404(User, name=form.data['username'])
            if user is not None:
                request.session['user'] = user.name
                request.session['user_id'] = user.id
                return HttpResponseRedirect('/quora/')
            else:
                messages.info(
                    request, 'Incorrect login details')
                return HttpResponseRedirect('/quora/loginpage')
        else:
            form = UserForm()
