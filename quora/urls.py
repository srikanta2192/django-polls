from django.conf.urls import url

from quora.login import LoginPageView, UserLoginView
from quora.signup import SignupView
from quora.views import IndexView
from quora.views_function.postsByUser import PostsByUserView
from quora.views_function.commentPage import CommentPageView
from quora.views_function.createComment import CreateCommentView
from quora.views_function.changePassword import ChangePasswordPage,ChangePasswordExecution
from quora.views_function.createPost import CreatePostView, CreatePostPageView
from quora.views_function.createUser import CreateUserView
from quora.views_function.like import LikeView
from quora.views_function.editPostPage import EditPostPageView
from quora.views_function.editPostSave import EditPostSaveView
from quora.views_function.editComment import EditCommentPageView, EditCommentExecutionView
from quora.views_function.userList import UserListView

from . import views

app_name = 'quora'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<post_id>[0-9]+)/$', views.viewPost, name='viewPost'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^loginpage/$', LoginPageView.as_view(), name='loginpage'),
    url(r'^userlogin/$', UserLoginView.as_view(), name='userLogin'),
    url(r'^userlogout/$', views.userLogout, name='userLogout'),
    url(r'^changePasswordPage/$', ChangePasswordPage.as_view(),
        name='changePasswordPage'),
    url(r'^changePassword/$', ChangePasswordExecution.as_view(), name='changePassword'),
    url(r'^(?P<username>[a-zA-Z0-9]+)/userPosts/$',
        PostsByUserView.as_view(), name='userPosts'),
    url(r'^(?P<post_id>[0-9]+)/commentPage/$',
        CommentPageView.as_view(), name='commentPage'),
    url(r'^(?P<post_id>[0-9]+)/createComment/$',
        CreateCommentView.as_view(), name='createComment'),
    url(r'^createuser/$', CreateUserView.as_view(), name='createUser'),
    url(r'^createPost/$', CreatePostView.as_view(), name='createPost'),
    url(r'^createPostPage/$', CreatePostPageView.as_view(), name='createPostPage'),
    url(r'^(?P<post_id>[0-9]+)/like/$',
        LikeView.as_view(), name='like'),
    url(r'^(?P<post_id>[0-9]+)/editPostPage/$',
        EditPostPageView.as_view(), name='editPostPage'),
    url(r'^(?P<post_id>[0-9]+)/editPostSave/$',
        EditPostSaveView.as_view(), name='editPostSave'),
    url(r'^(?P<post_id>[0-9]+)/(?P<comment_id>[0-9]+)/editCommentPage/$',
        EditCommentPageView.as_view(), name='editCommentPage'),
    url(r'^(?P<comment_id>[0-9]+)/editComment/$',
        EditCommentExecutionView.as_view(), name='editComment'),
    url(r'^users/$', UserListView.as_view(), name='users')
]
