from rest_framework import serializers

from core.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
        ]
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value
    def validate_password(self, value):
        """Validate the password"""
        # Check length of password
        if len(value) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters long"
            )
        # Check password match with confirm password
        if value != self.initial_data.get("confirm_password"):
            raise serializers.ValidationError(
                "Password and confirm password don't match"
            )
        return value

    def create(self, validated_data):
        """Create a new user"""
        # Remove confirm_password from validated_data
        validated_data.pop("confirm_password", None)

        # return super().create(validated_data)
# Use create_user to properly hash the password
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user
