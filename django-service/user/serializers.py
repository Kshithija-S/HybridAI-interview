from rest_framework import serializers

class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)
    full_name = serializers.CharField(max_length=100, allow_blank=True)

    def validate_password(self, value):
        # Custom validation for password
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value

class UserResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    full_name = serializers.CharField(allow_blank=True, allow_null=True)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField()

    def validate(self, data):
        # Either username or email must be provided
        if not data.get('username') and not data.get('email'):
            raise serializers.ValidationError("Either username or email must be provided")
        return data