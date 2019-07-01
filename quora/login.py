from django.views import generic
from django.shortcuts import render, get_object_or_404
from quora.views import current_user
from quora.forms import UserForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from quora.models import User
from django.contrib import messages

class LoginPageView(generic.View):

    def get(self, request):
        user = current_user(request)

        return render(request, 'quora/login.html', {
            'username': user['user']
        })


class UserLoginView(generic.View):
    def post(self, request):
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
