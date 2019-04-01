from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import views
from rest_framework.decorators import api_view

from django.contrib.auth.models import User

from .models import (
                    Post, 
                    Video, 
                    PostLike, 
                    PostComment, 
                    CommentComment, 
                    PostCommentLike, 
                    UserFollow, 
                    PlayList, 
                    CommentCommentLike,
                    NotificationPermission
                )
from .serializers import (
                    PostSerializer,
                    PostLikeSerializer, 
                    PostCommentSerializer, 
                    CommentCommentSerializer, 
                    VideoSerializer, 
                    PostCommentLikeSerializer, 
                    UserFollowSerializer, 
                    PlayListSerializer, 
                    CommentCommentLikeSerializer, 
                    CurrentUserSerializer,
                    NotificationPermissionSerializer
                )

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    

class PostLikeViewSet(viewsets.ModelViewSet):

    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = (IsAuthenticated,)


class PostCommentViewSet(viewsets.ModelViewSet):

    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    permission_classes = (IsAuthenticated,)


class CommentCommentViewSet(viewsets.ModelViewSet):

    queryset = CommentComment.objects.all()
    serializer_class = CommentCommentSerializer
    permission_classes = (IsAuthenticated,)


class VideoViewSet(viewsets.ModelViewSet):

    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (IsAuthenticated,)


class PostCommentLikeViewSet(viewsets.ModelViewSet):

    queryset = PostCommentLike.objects.all()
    serializer_class = PostCommentLikeSerializer
    permission_classes = (IsAuthenticated,)


class CommentCommentLikeViewSet(viewsets.ModelViewSet):

    queryset = CommentCommentLike.objects.all()
    serializer_class = CommentCommentLikeSerializer
    permission_classes = (IsAuthenticated,)


class UserFollowViewSet(viewsets.ModelViewSet):

    queryset = UserFollow.objects.all()
    serializer_class = UserFollowSerializer
    permission_classes = (IsAuthenticated,)


class PlayListViewSet(viewsets.ModelViewSet):

    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer
    permission_classes = (IsAuthenticated,)



class NotificationPermissionViewSet(views.APIView):

    queryset = NotificationPermission.objects.all()
    serializer_class = NotificationPermissionSerializer

    def post(self, request, device_id, format=None):

        if NotificationPermission.objects.filter(device_id=device_id).count() > 0:
            instance = NotificationPermission.objects.get(device_id=device_id)
            serializer = NotificationPermissionSerializer(
                instance=instance,
                data=request.data
            )
        else:
            serializer = NotificationPermissionSerializer(
                data=request.data
            )
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserInfoView(views.APIView):
    
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, format=None):
        
        count_posts = Post.objects.filter(author=id).count()
        count_following = UserFollow.objects.filter(follower=id).count()
        count_follower = UserFollow.objects.filter(following=id).count()

        content = {
            'num_of_posts': count_posts,
            'num_of_following': count_following,
            'num_of_followers': count_follower,
        }

        return Response(content)
    
    
class PostInfoView(views.APIView):
    
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, format=None):
        count_post_like = PostLike.objects.filter(post=id).count()
        count_post_comment = PostComment.objects.filter(post=id).count()

        content = {
            'num_of_likes': count_post_like,
            'num_of_comment': count_post_comment,
        }

        return Response(content)


class PlayListView(views.APIView):
    
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id, format=None):

        playlist = PlayList.objects.filter(owner=user_id)
        values = PlayListSerializer(data=playlist)
        values.is_valid()

        return Response(values.data)


# Shares part
"""
Sharing Profile(User by username), Sharing Post, Sharing Video
"""


class SharingProfile(views.APIView):

    def get(self, request, username, format=None):
        profile = User.objects.filter(username=username)
        value = CurrentUserSerializer(data=profile, many=True)
        value.is_valid()

        return Response(value.data[0])


class SharingPost(views.APIView):

    def get(self, request, hashtag, format=None):
        post = Post.objects.filter(link_ref=hashtag)
        value = PostSerializer(data=post, many=True)
        value.is_valid()

        return Response(value.data[0])


class SharingVideo(views.APIView):

    def get(self, request, videotag, format=None):
        video = Video.objects.filter(link_ref=videotag)
        value = VideoSerializer(data=video, many=True)
        value.is_valid()

        return Response(value.data[0])


class CommentsByPost(views.APIView):

    def get(self, request, post_id, format=None):
        comments = PostComment.objects.filter(post=post_id).order_by('created_at')
        value = PostCommentSerializer(data=comments, many=True)
        value.is_valid()

        return Response(value.data)

