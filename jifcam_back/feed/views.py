from django.shortcuts import render
from django.db.models import Count

from django.views.decorators.csrf import csrf_exempt
from rest_framework import views,viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from posts.models import Post, UserFollow
from posts.serializers import PostSerializer, CurrentUserSerializer
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponseRedirect

# Create your views here.

class TrendingView(views.APIView):

    def get(self, request, format=None):
        time_threshold = timezone.now() - timedelta(hours=4)
        posts_in_4_hour = Post.objects.filter(created_at__gt=time_threshold)
        print(time_threshold)
        value = PostSerializer(data=posts_in_4_hour, many=True)
        value.is_valid()

        return Response(value.data)


class FollowerPostView(views.APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        posts = []
        for user in request.user.follower.all():
            for post in Post.objects.filter(author=user.following):
                posts.append(post)
        serializer = PostSerializer(
            data=posts,
            many=True
        )
        serializer.is_valid()

        return Response(serializer.data)

    
class MostPostedUsersView(views.APIView):

    def get(self, request, format=None):
        sorted_users = User.objects.annotate(num_views=Count('post_author')).filter(is_superuser=False).order_by('-num_views')
        serializer = CurrentUserSerializer(
            data=sorted_users,
            many=True
        )
        serializer.is_valid()

        return Response(serializer.data)


class UserSearchView(views.APIView):

    def post(self, request, format=None):
        search_param = request.POST.get('username')
        print(search_param)
        search_users = User.objects.filter(username__contains=search_param)

        serializer = CurrentUserSerializer(
            data=search_users,
            many=True
        )
        serializer.is_valid()

        return Response(serializer.data)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def download(request):
    return HttpResponseRedirect(redirect_to='http://jifcam.com/test')