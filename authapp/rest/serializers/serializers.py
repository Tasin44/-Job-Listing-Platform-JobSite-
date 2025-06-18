from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from core.models import User, UserProfile
from core.choices import UserRoleChoices
from authapp.utils import EmailService


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    Handles password confirmation and role validation
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    role = serializers.ChoiceField(choices=UserRoleChoices.choices, required=True)
    class Meta:
        model = User
        fields = [
            "username",'first_name', 'last_name','email', 'phone',
            'password', 'password_confirm', 'role'
        ]
        extra_kwargs = {
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        """Validate password confirmation and email uniqueness"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")

        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        

        return attrs

    def create(self, validated_data):
        """Create user and send welcome email"""
        validated_data.pop('password_confirm')  # Remove password_confirm
        
        user = User.objects.create_user(**validated_data)
        
        EmailService.send_welcome_email(user)
        
        return user


class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        """Authenticate user credentials"""
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )

            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')

            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include email and password.')


class PasswordResetRequestSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, value):

        try:
            user = User.objects.get(email=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

    def save(self):

        email = self.validated_data['email']
        user = User.objects.get(email=email)
        

        token = default_token_generator.make_token(user)
        

        EmailService.send_password_reset_email(user, token)
        
        return user


class PasswordResetConfirmSerializer(serializers.Serializer):

    new_password = serializers.CharField(
        min_length=8,
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        style={'input_type': 'password'}
    )
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):

        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        

        try:
            validate_password(attrs['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError({'new_password': e.messages})
        

        try:
            uid = force_str(urlsafe_base64_decode(attrs['uid']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('Invalid reset link.')
        
        if not default_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError('Invalid or expired reset link.')
        
        attrs['user'] = user
        return attrs

    def save(self):

        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):

    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_role = serializers.CharField(source='user.role', read_only=True)
    skills_list = serializers.ListField(source='get_skills_list', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'user_email', 'user_name', 'user_role', 'photo', 'bio',
            'date_of_birth', 'gender', 'address', 'city', 'country',
            'resume', 'skills', 'skills_list', 'experience_years'
        ]
        extra_kwargs = {
            'photo': {'required': False},
            'resume': {'required': False},
        }


class UserSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'uid', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'role', 'is_email_verified', 'created_at', 'profile'
        ]
        read_only_fields = ['uid', 'email', 'created_at', 'is_email_verified']
    def get_profile(self, obj):
            try:
                return UserProfileSerializer(obj.profile).data
            except UserProfile.DoesNotExist:
                return None