from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField, ArrayField

import uuid
import os

def get_video_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "video/%s.%s" % (uuid.uuid4(), ext)
    return filename


def get_thumb_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "thumbs/%s.%s" % (uuid.uuid4(), ext)
    return filename

# Create your models here.

class Video(models.Model):

    maintag = models.CharField(max_length=200)
    subtags = JSONField(default=list)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.FileField(upload_to=get_video_path, verbose_name='Post Video')
    thumbnail = models.ImageField(upload_to=get_thumb_path, verbose_name='Video Thumbnail')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    link_ref = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)

    def __str__(self):
        return self.maintag


class Post(models.Model):

    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, related_name="post_author", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video = models.OneToOneField(Video, on_delete=models.CASCADE)
    is_active = models.BooleanField('Show/Hide', default=True)
    link_ref = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)

    def __str__(self):
        return self.title


class PostLike(models.Model):

    like_user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.like_user+" likes "+self.post


class PostComment(models.Model):

    author=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    text=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return " commented "+self.post.__str__()


class CommentComment(models.Model):

    author=models.ForeignKey(User, on_delete=models.CASCADE)
    comment=models.ForeignKey(PostComment, related_name='childs', on_delete=models.CASCADE)
    text=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return " commented - comment "+self.comment


class PostCommentLike(models.Model):

    like_user=models.ForeignKey(User, on_delete=models.CASCADE)
    comment=models.ForeignKey(PostComment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.like_user.__str__()+" likes - comment(post) "+self.comment


class CommentCommentLike(models.Model):

    like_user=models.ForeignKey(User, on_delete=models.CASCADE)
    comment=models.ForeignKey(CommentComment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.like_user.__str__()+" likes - comment(comment) "+self.comment


class UserFollow(models.Model):

    follower=models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    following=models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.follower.__str__()+" follows "+self.following.__str__()


class PlayList(models.Model):

    owner=models.ForeignKey(User, related_name="playlist_owner", on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner+" save "+self.video+" in his/her playlist"


class NotificationPermission(models.Model):

    device_id = models.CharField(blank=True, unique=True, default=None, max_length=255)
    is_enabled = models.BooleanField(default=True)
    duration = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

