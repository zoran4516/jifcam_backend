from django.urls import path, include
from .views import (
                PostViewSet,
                PostLikeViewSet,
                PostCommentViewSet, 
                CommentCommentViewSet, 
                VideoViewSet, 
                PostCommentLikeViewSet, 
                UserFollowViewSet, 
                PostInfoView, 
                UserInfoView, 
                PlayListViewSet, 
                PlayListView, 
                CommentCommentLikeViewSet,
                SharingProfile,
                SharingPost,
                SharingVideo,
                NotificationPermissionViewSet,
                CommentsByPost
            ) 
                
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'like', PostLikeViewSet)
router.register(r'comment', PostCommentViewSet)
router.register(r'comments/comment', CommentCommentViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'comments/post/like', PostCommentLikeViewSet)
router.register(r'comments/comment/like', CommentCommentViewSet)
router.register(r'users/follow', UserFollowViewSet)
router.register(r'playlists', PlayListViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('user/<int:id>', UserInfoView.as_view()),
    path('post/<int:id>', PostInfoView.as_view()),
    path('playlist/<int:user_id>', PlayListView.as_view()),
    path('share/profile/<slug:username>', SharingProfile.as_view()),
    path('share/post/<slug:hashtag>', SharingPost.as_view()),
    path('share/video/<slug:videotag>', SharingVideo.as_view()),
    path('notification/enable/<slug:device_id>', NotificationPermissionViewSet.as_view()),
    path('comments/<int:post_id>', CommentsByPost.as_view()),
]