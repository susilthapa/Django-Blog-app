from django.urls import path
from .views import (
    UserCreateAPIView,
    UserLoginAOIView,
    UserProfileUpdateAPIView
)
from rest_framework.authtoken import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='api-register'),
    path('login/', UserLoginAOIView.as_view(), name='api-login'),
    path('profile/', UserProfileUpdateAPIView.as_view(), name='api-profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]