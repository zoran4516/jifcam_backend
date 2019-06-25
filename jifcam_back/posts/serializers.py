from rest_framework  import serializers
from django.contrib.auth.models import User
from .models import (
                Post, 
                PostLike, 
                PostComment, 
                CommentComment, 
                Video, 
                PostCommentLike, 
                UserFollow, 
                PlayList, 
                CommentCommentLike,
                NotificationPermission
            )

class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model=Video
        fields=('id', 'maintag', 'owner', 'video', 'subtags', 'thumbnail', 'created_at', 'updated_at')

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'video', 'created_at', 'updated_at', 'link_ref')


class PostLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model=PostLike
        fields=('id', 'like_user', 'post', 'created_at', 'updated_at')


class CommentCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model=CommentComment
        fields=('id', 'author', 'comment', 'text', 'created_at', 'updated_at')



class PostCommentSerializer(serializers.ModelSerializer):

    childs = CommentCommentSerializer(many=True, read_only=True)

    class Meta:
        model=PostComment
        fields=('id', 'author', 'post', 'text', 'childs', 'created_at', 'updated_at')


class PostCommentLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model=PostCommentLike
        fields=('id', 'like_user', 'comment', 'created_at', 'updated_at')


class CommentCommentLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model=CommentCommentLike
        fields=('id', 'like_user', 'comment', 'created_at', 'updated_at')


class UserFollowSerializer(serializers.ModelSerializer):

    class Meta:
        model=UserFollow
        fields=('id', 'follower', 'following', 'created_at', 'updated_at')


class PlayListSerializer(serializers.ModelSerializer):

    class Meta:
        model=PlayList
        fields=('id', 'owner', 'video', 'created_at', 'updated_at')


class CurrentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=('username', 'email', 'date_joined', 'first_name', 'last_name')
    

class NotificationPermissionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=NotificationPermission
        fields=('device_id', 'is_enabled', 'duration', 'created_at', 'updated_at')

