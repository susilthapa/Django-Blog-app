from django.urls import path
from .views import (
    UserCreateAPIView,
    UserLoginAOIView,
)

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='api-register'),
    path('login/', UserLoginAOIView.as_view(), name='api-login'),

]