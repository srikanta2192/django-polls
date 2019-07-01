from quora.models import User
from django.http import HttpResponse
from django.views import generic


class UserListView(generic.View):
    def get(self, request):
        user_list = User.objects.order_by('-user_created_at')
        output = (', ').join([u.name for u in user_list])

        return HttpResponse(output)
