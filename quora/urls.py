from django.conf.urls import url

from quora.login import LoginPageView
from quora.signup import SignupView
from quora.views import IndexView, userLogout, viewPost
from quora.views_function.changePassword import ChangePasswordPage
from quora.views_function.comment.commentPage import CommentPageView
from quora.views_function.comment.create import CreateCommentView
from quora.views_function.post.create import CreatePostView
from quora.views_function.createUser import CreateUserView
from quora.views_function.comment.edit import EditCommentPageView
from quora.views_function.post.editPage import EditPostPageView
from quora.views_function.post.editSave import EditPostSaveView
from quora.views_function.like import LikeView
from quora.views_function.post.byUser import PostsByUserView

app_name = 'quora'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<post_id>[0-9]+)/$', viewPost, name='viewPost'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^loginpage/$', LoginPageView.as_view(), name='loginpage'),
    url(r'^user/login/$', LoginPageView.as_view(), name='userLogin'),
    url(r'^user/logout/$', userLogout, name='userLogout'),
    url(r'^password/change/$', ChangePasswordPage.as_view(),
        name='changePasswordPage'),
    url(r'^password/change/save/$', ChangePasswordPage.as_view(), name='changePassword'),
    url(r'^(?P<username>[a-zA-Z0-9]+)/userPosts/$',
        PostsByUserView.as_view(), name='userPosts'),
    url(r'^(?P<post_id>[0-9]+)/comment/$',
        CommentPageView.as_view(), name='commentPage'),
    url(r'^(?P<post_id>[0-9]+)/createComment/$',
        CreateCommentView.as_view(), name='createComment'),
    url(r'^user/create/$', CreateUserView.as_view(), name='createUser'),
    url(r'^post/create/save/$', CreatePostView.as_view(), name='createPost'),
    url(r'^post/create$', CreatePostView.as_view(), name='createPostPage'),
    url(r'^(?P<post_id>[0-9]+)/like/$',
        LikeView.as_view(), name='like'),
    url(r'^(?P<post_id>[0-9]+)/post/edit/$',
        EditPostPageView.as_view(), name='editPostPage'),
    url(r'^(?P<post_id>[0-9]+)/post/save/$',
        EditPostSaveView.as_view(), name='editPostSave'),
    url(r'^(?P<post_id>[0-9]+)/(?P<comment_id>[0-9]+)/comment/edit/$',
        EditCommentPageView.as_view(), name='editCommentPage'),
    url(r'^(?P<comment_id>[0-9]+)/comment/edit/save/$',
        EditCommentPageView.as_view(), name='editComment'),
    # url(r'^users/$', UserListView.as_view(), name='users')
]
