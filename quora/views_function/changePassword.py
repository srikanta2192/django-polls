
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required


from quora.models import Comment, Post
from quora.views import current_user
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import check_password
from quora.models import Comment, Post
from django.contrib.auth import update_session_auth_hash
from quora.views import current_user
from django.contrib.auth import authenticate, get_user, login


class ChangePasswordPage(generic.View):

    @method_decorator(login_required)
    def get(self, request):
        user = get_user(request)
        if user is not None:
            template = 'quora/password/change.html'
            context = {
                'username': user.username}
            return render(request, template, context)
        else:
            template = 'quora/login.html'
            messages.info(request, "Please login to continue")
            return render(request, template)

    @method_decorator(login_required)
    def post(self, request):
        user = get_user(request)
        if user is not None:
            if request.method == 'POST':
                context = {'username': user.username}
                template = 'quora/password/change.html'
                user = get_user(request)
                currentPassword = user.password
                passwordCheck = check_password(request.POST['oldPassword'], currentPassword)
                if passwordCheck:
                    newPassword = request.POST['newPassword']
                    confirmPassword = request.POST['confirmPassword']
                    if newPassword == confirmPassword:
                        template = 'quora/login.html'
                        user.password = newPassword
                        user.set_password(newPassword)
                        user.save()
                        update_session_auth_hash(request, user)
                        messages.success(
                            request, 'Password successfully changed')
                        return render(request, template)
                    else:

                        messages.info(
                            request, 'New password and confirm password don\'t match')
                        return render(request, template, context)
                else:
                    messages.info(
                        request, 'Old Password is incorrect')
                    return render(request, template, context)
        else:
            messages.info(request, "Please login to continue")
            return render(request, 'quora/login.html')
