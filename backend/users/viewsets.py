import datetime
from urllib.request import Request

from django.contrib.auth import authenticate, login
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common.utils import generate_4_symbols_code, send_code
from .models import User, AuthenticationCode
from .serializers import AuthenticationGetPhoneSerializer, AuthenticationGetCodeCodeSerializer


@extend_schema(tags=["User"])
class AuthenticationViewSet(GenericViewSet):
    """Вьюсет пользователя."""

    def get_serializer_class(self):
        if self.action == "get_code":
            return AuthenticationGetPhoneSerializer
        if self.action == "validate_code":
            return AuthenticationGetCodeCodeSerializer

    def get_queryset(self):
        if self.action in ["get_code", "validate_code"]:
            return User.objects.all()

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

        if validation_code.code != serializer.data["code"]:
            return Response({"error": "Неверный код авторизации"}, status=status.HTTP_400_BAD_REQUEST)
        elif validation_code.created_at + datetime.timedelta(minutes=3) < datetime.datetime.now():
            return Response({"error": "Время действия кода истекло"}, status=status.HTTP_400_BAD_REQUEST)
        elif validation_code.is_activated:
            return Response({"error": "Код уже был использован"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone_number=serializer.data["phone_number"]).first()
        if user:
            user = authenticate(
                username=user.username,
                password="1111"
            )
        else:
            user = User(username=serializer.data["phone_number"], password="1111")
            user.save()

        validation_code.is_activated = True
        validation_code.save()
        login(request, user)
        return Response(serializer.data, status=status.HTTP_200_OK)
