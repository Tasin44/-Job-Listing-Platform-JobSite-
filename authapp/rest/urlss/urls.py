from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView

from authapp.rest.views.views import (
    UserRegistrationView,
    UserLoginView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    UserProfileView,
    current_user_view,
    logout_view,

)

urlpatterns = [
    # Authentication endpoints
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', logout_view, name='user-logout'),

    # JWT Token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Password reset endpoints
    path('forgot-password/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('reset-password/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    # User profile endpoints
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('me/', current_user_view, name='current-user'),
]