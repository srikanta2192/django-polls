from django.conf.urls import url

from . import views

app_name = 'quora'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<post_id>[0-9]+)/$', views.viewPost, name='viewPost'),
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^loginpage/$', views.loginPage, name='loginpage'),
    url(r'^userlogin/$', views.userLogin, name='userLogin'),
    url(r'^userlogout/$', views.userLogout, name='userLogout'),
    url(r'^(?P<username>[a-zA-Z0-9]+)/userPosts/$',
        views.userPosts, name='userPosts'),
    url(r'^(?P<post_id>[0-9]+)/commentPage/$',
        views.commentPage, name='commentPage'),
    url(r'^createuser/$', views.createUser, name='createuser'),
    url(r'^createPost/$', views.createPost, name='createPost'),
    url(r'^createPostPage/$', views.createPostPage, name='createPostPage'),
    url(r'^(?P<post_id>[0-9]+)/(?P<username>[A-Za-z0-9]+)/like/$',
        views.like, name='like'),
    url(r'^(?P<post_id>[0-9]+)/editPostPage/$',
        views.editPostPage, name='editPostPage'),
    url(r'^(?P<post_id>[0-9]+)/editPostSave/$',
        views.editPostSave, name='editPostSave'),
    url(r'^users/$', views.user_list, name='users'),
    url(r'^loginpage/$', views.loginPage, name='loginpage'),
    url(r'^userlogin/$', views.userLogin, name='userLogin'),
    url(r'^userlogout/$', views.userLogout, name='userLogout'),
]
