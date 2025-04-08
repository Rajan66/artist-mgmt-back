from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()
    last_login = serializers.DateTimeField()
    date_joined = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    is_active = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()


class UserOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()
    role = serializers.CharField()
    date_joined = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    is_active = serializers.BooleanField()


class UserProfileOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    user = UserSerializer()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    dob = serializers.DateTimeField()
    gender = serializers.CharField()
    address = serializers.CharField()
    phone = serializers.CharField()


class UserProfileSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    user = UserOutputSerializer()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    dob = serializers.DateTimeField()
    gender = serializers.CharField()
    address = serializers.CharField()
    phone = serializers.CharField()
