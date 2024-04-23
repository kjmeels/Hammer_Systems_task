from rest_framework import serializers

from users.models import User


class AuthenticationGetPhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=13, min_length=13)


class AuthenticationGetCodeCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=13, min_length=13)
    code = serializers.CharField(required=True, max_length=4, min_length=4)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
        )


class UserProfileSerializer(serializers.ModelSerializer):
    referral_users = UserListSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "username",
            "invite_code",
            "referral_users",
        )


class SendInviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField(required=True, max_length=6, min_length=6)
