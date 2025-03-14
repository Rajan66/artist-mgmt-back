from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()
    last_login = serializers.DateTimeField()
    date_joined = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    is_removed = serializers.BooleanField()
