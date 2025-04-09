from rest_framework import serializers, status
from users.models import CustomUser as User

from authentication.exceptions import CustomAuthenticationException


class UserLoginSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("Invalid crendentials.")

        if not user.check_password(password):
            flag = user.check_password(password)
            print(flag)
            raise serializers.ValidationError("Invalid password.")

        attrs["user"] = user
        return attrs


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]

        user = User.objects.create(email=email)
        user.set_password(password)
        user.save()

        return user

    def validate(self, attrs):
        password = attrs["password"]
        confirm_password = attrs["confirm_password"]

        if password != confirm_password:
            raise CustomAuthenticationException(
                detail="Passwords do not match",
                error_type="Authentication error",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["old_password"]

        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("Invalid email.")

        if not user.check_password(password):
            flag = user.check_password(password)
            print("Check password failed ==========> ", flag)
            raise serializers.ValidationError("Invalid password.")

        new_password = attrs["new_password"]
        confirm_password = attrs["confirm_password"]

        if new_password != confirm_password:
            raise CustomAuthenticationException(
                detail="Passwords do not match",
                error_type="Authentication error",
                code=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(new_password)
        user.save()

        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs["password"]
        confirm_password = attrs["confirm_password"]

        if password != confirm_password:
            raise CustomAuthenticationException(
                detail="Passwords do not match",
                error_type="Authentication error",
                code=status.HTTP_400_BAD_REQUEST,
            )

        return attrs
