from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import generic


from quora.forms import UserForm
from quora.models import User


class CreateUserView(generic.View):

    def post(self, request):
        if request.method == 'POST':
            form = UserForm(request.POST)
            try:
                if form.is_valid():
                    form.clean_message()
                    new_user = User.objects.create(
                        created_at=timezone.now(),
                        name=form.data['username'],
                        password=form.data['password'],
                    )
                    request.session['user'] = new_user.name
                    messages.success(request, "User created successfully")
                    return HttpResponseRedirect('/quora/')
            except IntegrityError as e:
                messages.info(request,
                            "Username exist! Please try with a different username")
                return HttpResponseRedirect("/quora/signup")
            except KeyError:
                messages.info(request,
                            "Please login")

                return HttpResponseRedirect("/quora/login")

        else:
            form = UserForm()
