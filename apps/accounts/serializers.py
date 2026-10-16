from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    firstName = serializers.CharField(write_only=True)
    lastName = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "firstName",
            "lastName",
            "email",
            "password",
            "confirmPassword",
        ]

    def validate(self, data):
        if User.objects.filter(username__iexact=data["username"]).exists():
            raise serializers.ValidationError({
                 "username": "This username is already taken."
        })

        if data["password"] != data["confirmPassword"]:
            raise serializers.ValidationError({
                "confirmPassword": "Passwords do not match."
            })

        if User.objects.filter(email__iexact=data["email"]).exists():
            raise serializers.ValidationError({
                "email": "An account with this email already exists."
            })

        if len(data["password"]) < 8: raise serializers.ValidationError({ "password": "Password must be at least 8 characters." })

        return data

    def create(self, validated_data):
        first_name = validated_data.pop("firstName")
        last_name = validated_data.pop("lastName")
        validated_data.pop("confirmPassword")
        password = validated_data.pop("password")
        

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        ]