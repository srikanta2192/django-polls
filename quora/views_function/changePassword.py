
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import generic

from quora.decorators import user_login_required
from quora.models import Comment, Post, User
from quora.views import current_user
from django.contrib.sessions.models import Session


class ChangePasswordPage(generic.View):

    @method_decorator(user_login_required)
    def get(self, request):
        current_user_details = current_user(request)
        if current_user_details['user'] is not None:
            return render(request, 'quora/changePasswordPage.html', {
                'username': current_user_details['user']})
        else:
            messages.info(request, "Please login to continue")
            return render(request, 'quora/login.html')


class ChangePasswordExecution(generic.View):

    def post(self, request):
        current_user_details = current_user(request)
        if current_user_details['user'] is not None:
            if request.method == 'POST':
                user = get_object_or_404(
                    User, name=current_user_details['user'])
                oldPassword = request.POST['oldPassword']
                if oldPassword == user.password:
                    newPassword = request.POST['newPassword']
                    confirmPassword = request.POST['confirmPassword']
                    if newPassword == confirmPassword:
                        user.password = newPassword
                        user.save()
                        messages.success(
                            request, 'Password successfully changed')
                        Session.objects.all().delete()
                        return render(request, 'quora/login.html')
                    else:
                        messages.info(
                            request, 'New password and confirm password don\'t match')
                        return render(request, 'quora/changePasswordPage.html', {'username': current_user_details['user']})
                else:
                    messages.info(
                        request, 'Password is incorrect')
                    return render(request, 'quora/changePasswordPage.html', {'username': current_user_details['user']})
        else:
            messages.info(request, "Please login to continue")
            return render(request, 'quora/login.html')
