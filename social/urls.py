from django.urls import path
from .views import *

#define url paths under the social app
urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile-edit'),
    path('profile/<int:pk>/friends/', FriendList.as_view(), name = 'friendlist'),
    path('profile/<int:pk>/friends/add', AddFriend.as_view(), name='add-as-friend'),
    path('profile/<int:pk>/friends/unfriend', Unfriend.as_view(), name='unfriend'),
    path('search/', SearchUser.as_view(), name="search-user"),
    path('mail/', ShowAllThreads.as_view(), name='mail'),
    path('mail/create-thread/', CreateThread.as_view(), name='create-thread'),
    path('mail/<int:pk>/', ViewThread.as_view(), name='thread'),
    path('mail/<int:pk>/create-message/', WriteNewMessage.as_view(), name='create-message'),

    path('post/<int:pk>/like', Like.as_view(), name='like'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_pk>/comment/<int:pk>/like', LikeComments.as_view(), name='comment-like'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:post_pk>/comment/<int:pk>/reply', CommentReplyView.as_view(), name='comment-reply'),
   
]