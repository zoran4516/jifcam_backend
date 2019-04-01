from django.urls import path, include

from .views import TrendingView, FollowerPostView, MostPostedUsersView, UserSearchView, download

urlpatterns = [
    path('trending/', TrendingView.as_view()),
    path('following/posts/', FollowerPostView.as_view()),
    path('users/most/', MostPostedUsersView.as_view()),
    path('search/user/', UserSearchView.as_view()),
    path('download/', download )
]