from django.contrib import messages
from django.contrib.auth import get_user, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.models import Session
from django.shortcuts import render
from django.views import generic


class ChangePasswordPage(LoginRequiredMixin, generic.View):

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

    def post(self, request):
        user = get_user(request)
        if user is not None:
            if request.method == 'POST':
                context = {'username': user.username}
                template = 'quora/password/change.html'
                user = get_user(request)
                currentPassword = user.password
                passwordCheck = check_password(
                    request.POST['oldPassword'], currentPassword)
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
