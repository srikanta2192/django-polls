from django.conf.urls import url

from . import views

app_name = 'quora'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^loginpage/$', views.loginPage, name='loginpage'),
    url(r'^userlogin/$', views.userLogin, name='userLogin'),
    url(r'^userlogout/$', views.userLogout, name='userLogout'),
    url(r'^createuser/$', views.createUser, name='createuser'),
    url(r'^createPost/$', views.createPost, name='createPost'),
    url(r'^createPostPage/$', views.createPostPage, name='createPostPage'),
    url(r'^(?P<post_id>[0-9]+)/editPostPage/$', views.editPostPage, name='editPostPage'),
    url(r'^users/$', views.user_list, name='users'),
    url(r'^loginpage/$', views.loginPage, name='loginpage'),
    url(r'^userlogin/$', views.userLogin, name='userLogin'),
    url(r'^/userlogout/$', views.userLogout, name='userLogout'),
]
