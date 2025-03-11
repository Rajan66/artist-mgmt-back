from rest_framework import serializers
from users.models import CustomUser as User


class UserLoginSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("Invalid crendentials.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password.")

        attrs["user"] = user
        return attrs


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
