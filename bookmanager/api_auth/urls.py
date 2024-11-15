from django.urls import path
from .views import CreateUserAPIView

urlpatterns = [
    path('register/', CreateUserAPIView.as_view(), name='user-register'),
]