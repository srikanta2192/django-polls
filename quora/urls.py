from django.conf.urls import url

from . import views

app_name = 'quora'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<post_id>[0-9]+)/$', views.viewPost, name='viewPost'),
    url(r'^signup/$', views.signUp, name='signup'),
    url(r'^loginpage/$', views.loginPage, name='loginpage'),
    url(r'^userlogin/$', views.userLogin, name='userLogin'),
    url(r'^userlogout/$', views.userLogout, name='userLogout'),
    url(r'^changePasswordPage/$', views.changePasswordPage, name='changePasswordPage'),
    url(r'^changePassword/$', views.changePassword, name='changePassword'),
    url(r'^(?P<username>[a-zA-Z0-9]+)/userPosts/$', views.postsByUser, name='userPosts'),
  
    url(r'^(?P<post_id>[0-9]+)/commentPage/$',
        views.commentPage, name='commentPage'),
    url(r'^(?P<post_id>[0-9]+)/createComment/$',
        views.createComment, name='createComment'),
    url(r'^createuser/$', views.createUser, name='createUser'),
    url(r'^createPost/$', views.createPost, name='createPost'),
    url(r'^createPostPage/$', views.createPostPage, name='createPostPage'),
    url(r'^(?P<post_id>[0-9]+)/like/$',
        views.like, name='like'),
    url(r'^(?P<post_id>[0-9]+)/editPostPage/$',
        views.editPostPage, name='editPostPage'),
    url(r'^(?P<post_id>[0-9]+)/editPostSave/$',
        views.editPostSave, name='editPostSave'),
    url(r'^(?P<post_id>[0-9]+)/(?P<comment_id>[0-9]+)/editCommentPage/$',
        views.editCommentPage, name='editCommentPage'),
    url(r'^(?P<comment_id>[0-9]+)/editComment/$',
        views.editComment, name='editComment'),
    url(r'^users/$', views.user_list, name='users')
]
