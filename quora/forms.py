from django import forms
from quora.models import User, Post


class UserForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=100)

    def clean_message(self):
        password = self.cleaned_data['password']
        username = self.cleaned_data['username']
        try:
            if User.objects.filter(name=username).exists():
                raise forms.ValidationError("Username exists")
            return username
        except:
            pass


class PostForm(forms.Form):
    title = forms.CharField(max_length=200)
    content = forms.CharField(max_length=400)
