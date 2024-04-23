from rest_framework import serializers


class AuthenticationGetPhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=13, min_length=13)


class AuthenticationGetCodeCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=13, min_length=13)
    code = serializers.CharField(required=True, max_length=4, min_length=4)
