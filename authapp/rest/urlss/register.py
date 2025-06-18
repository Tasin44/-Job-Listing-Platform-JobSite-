from django.urls import path, include
from authapp.rest.views.views import UserRegistrationView

urlpatterns = [
    path("", UserRegistrationView.as_view(), name="user-register"),
]
