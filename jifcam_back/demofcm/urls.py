from django.urls import path, include
from .views import DemoView

urlpatterns = [
    path('', DemoView.as_view(), name='demo'),
]