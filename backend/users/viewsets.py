import datetime
from urllib.request import Request

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common.utils import generate_4_symbols_code, send_code, get_invite_code
from .models import User, AuthenticationCode
from .serializers import (
    AuthenticationGetPhoneSerializer,
    AuthenticationGetCodeCodeSerializer,
    UserProfileSerializer,
    SendInviteCodeSerializer,
)


@extend_schema(tags=["User"])
class AuthenticationViewSet(GenericViewSet):
    """Вьюсет пользователя."""

    lookup_field = "username"

    def get_permissions(self):
        if self.action in ["retrieve", "send_invite_code"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == "get_code":
            return AuthenticationGetPhoneSerializer
        if self.action == "validate_code":
            return AuthenticationGetCodeCodeSerializer
        if self.action == "retrieve":
            return UserProfileSerializer
        if self.action == "send_invite_code":
            return SendInviteCodeSerializer

    def get_queryset(self):
        return User.objects.all()

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        instance.referral_users = User.objects.filter(referral_code=instance.invite_code)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"])
    def get_code(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_code = AuthenticationCode(phone_number=serializer.data["phone_number"], code=generate_4_symbols_code())
        create_code.save()
        send_code()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["POST"])
    def validate_code(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validation_code = AuthenticationCode.objects.filter(phone_number=serializer.data["phone_number"]).last()

        if not validation_code:
            return Response({"error": "Неправильно введен номер"}, status=status.HTTP_400_BAD_REQUEST)
        elif validation_code.code != serializer.data["code"]:
            return Response({"error": "Неверный код авторизации"}, status=status.HTTP_400_BAD_REQUEST)
        elif validation_code.created_at + datetime.timedelta(minutes=5) < datetime.datetime.now(tz=datetime.UTC):
            return Response({"error": "Время действия кода истекло"}, status=status.HTTP_400_BAD_REQUEST)
        elif validation_code.is_activated:
            return Response({"error": "Код уже был использован"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=serializer.data["phone_number"]).first()
        if user:
            user = authenticate(
                username=user.username,
                password="1111"
            )
        else:
            user = User(
                username=serializer.data["phone_number"], password=make_password("1111"), invite_code=get_invite_code()
            )
            user.save()

        validation_code.is_activated = True
        validation_code.save()
        login(request, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["POST"])
    def send_invite_code(self, request: Request, *args, **kwargs) -> Response:
        user = self.request.user
        if user.referral_code:
            return Response({"error": "Инвайт-код уже был введен"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        referral_user = User.objects.filter(invite_code=serializer.data["invite_code"]).first()
        if referral_user == user:
            return Response({"error": "Пришлите код другого пользователя"}, status=status.HTTP_400_BAD_REQUEST)

        if referral_user:
            user.referral_code = referral_user.invite_code
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Пользователя с таким инвайт-кодом не существует"}, status=status.HTTP_404_NOT_FOUND)
