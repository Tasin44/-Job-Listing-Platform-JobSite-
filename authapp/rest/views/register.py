from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from authapp.rest.serializers.serializers import UserRegistrationSerializer

class UserRegisterView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]