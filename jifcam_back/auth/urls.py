from django.urls import path, include

from .views import login,signup

urlpatterns = [
    path('api/login/', login),
    path('api/join/', signup)
]