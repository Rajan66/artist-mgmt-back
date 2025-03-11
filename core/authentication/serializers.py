from rest_framework import serializers
from users.models import CustomUser as User


class UserLoginSerializer(serializers.Serializer):
    id = serializers.UUIDField(format="hex", read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return User(**validated_data)


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
