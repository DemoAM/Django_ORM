from rest_framework import serializers

from account.models import User
from account.models import Role


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "email", "password"]

        read_only_fields = [
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
        ]

    def validate_email(self, value):
        return value.strip().lower()

    def create(self, validated_data):
        validated_data["role"] = Role.Roles.ADMIN
        user = User.objects.create_user(**validated_data)
        return user


class EmployeeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "email", "password"]
        read_only_fields = [
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
            "role",
        ]

    def validate_email(self, value):
        return value.strip().lower()

    def create(self, validated_data):
        validated_data["role"] = Role.Roles.EMPLOYEE

        user = User.objects.create_user(**validated_data)

        return user


class LoginSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ["email", "password"]
