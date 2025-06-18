from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.models import User
from authapp.rest.serializers.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    UserSerializer,
    UserProfileSerializer
)


class UserRegistrationView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user with a specified role (Recruiter or Candidate)",
        responses={
            201: openapi.Response(
                description="User registered successfully",
                examples={
                    "application/json": {
                        "message": "User registered successfully",
                        "user": {
                            "uid": "uuid-here",
                            "email": "user@example.com",
                            "first_name": "John",
                            "last_name": "Doe",
                            "role": "CANDIDATE"
                        }
                    }
                }
            ),
            400: "Bad Request - Validation errors"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):

    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Authenticate user and get JWT tokens",
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "message": "Login successful",
                        "user": {
                            "uid": "uuid-here",
                            "email": "user@example.com",
                            "role": "CANDIDATE"
                        },
                        "tokens": {
                            "access": "jwt-access-token",
                            "refresh": "jwt-refresh-token"
                        }
                    }
                }
            ),
            400: "Bad Request - Invalid credentials"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)


class PasswordResetRequestView(generics.GenericAPIView):

    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Request password reset email",
        responses={
            200: openapi.Response(
                description="Password reset email sent",
                examples={
                    "application/json": {
                        "message": "Password reset email sent successfully"
                    }
                }
            ),
            400: "Bad Request - Email not found"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'Password reset email sent successfully'
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Confirm password reset with token",
        responses={
            200: openapi.Response(
                description="Password reset successful",
                examples={
                    "application/json": {
                        "message": "Password reset successful"
                    }
                }
            ),
            400: "Bad Request - Invalid token or validation errors"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'Password reset successful'
        }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Get the profile of the current user"""
        '''
        # profile, created = self.request.user.profile.get_or_create(
        #     user=self.request.user
        # )
        # return profile
        i got error for them 
        AttributeError: 'UserProfile' object has no attribute 'get_or_create'
        500 internal server error
        This happens because:

    In your get_object() method, you're calling get_or_create() on request.user.profile

    But request.user.profile already returns a UserProfile instance (not a manager)

    The get_or_create() method is only available on model managers (like UserProfile.objects), not on model instances

Root Causes

    Signal Conflict: Your core/signals.py already creates a profile automatically when a user is created

    Redundant Check: Your view tries to create a profile if it doesn't exist, but the signal already ensures it exists

    Incorrect Method Usage: You're trying to use a manager method (get_or_create) on a model instance
        '''
        return self.request.user.profile

    @swagger_auto_schema(
        operation_description="Get user profile information",
        responses={
            200: UserProfileSerializer,
            401: "Unauthorized"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update user profile information",
        responses={
            200: UserProfileSerializer,
            400: "Bad Request - Validation errors",
            401: "Unauthorized"
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update user profile information",
        responses={
            200: UserProfileSerializer,
            400: "Bad Request - Validation errors",
            401: "Unauthorized"
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


@swagger_auto_schema(
    method='get',
    operation_description="Get current user information",
    responses={
        200: UserSerializer,
        401: "Unauthorized"
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    print(f"Authenticated user: {request.user}")  # Debugging   
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    operation_description="Logout user (blacklist refresh token)",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token')
        },
        required=['refresh']
    ),
    responses={
        200: openapi.Response(
            description="Logout successful",
            examples={
                "application/json": {
                    "message": "Logout successful"
                }
            }
        ),
        400: "Bad Request - Invalid token"
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):

    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except Exception:
        return Response({
            'error': 'Invalid token'
        }, status=status.HTTP_400_BAD_REQUEST)