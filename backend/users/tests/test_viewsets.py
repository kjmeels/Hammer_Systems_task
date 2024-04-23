import datetime
from functools import partial

from django.contrib.auth.hashers import make_password
from pytest import mark
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from common.utils import get_invite_code
from users.models import AuthenticationCode, User
from users.tests.factories import UserFactory, AuthenticationCodeFactory


@mark.django_db
class TestUserViewSet(APITestCase):
    def setUp(self):
        self.get_code_url: str = reverse("users-get-code")
        self.validate_code_url: str = reverse("users-validate-code")
        self.retrieve_url = partial(reverse, "users-detail")
        self.send_invite_code_url: str = reverse("users-send-invite-code")

    def test_get_code(self):
        payload = {"phone_number": "+375291234567"}

        with self.assertNumQueries(1):
            res = self.client.post(self.get_code_url, payload)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AuthenticationCode.objects.count(), 1)
        self.assertEqual(res_json["phone_number"], AuthenticationCode.objects.first().phone_number)

    def test_validate_code(self):
        authentication_code = AuthenticationCodeFactory(phone_number="+375291234567")
        payload = {"phone_number": authentication_code.phone_number, "code": authentication_code.code}

        with self.assertNumQueries(5):
            res = self.client.post(self.validate_code_url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        created_user = User.objects.first()
        self.assertTrue(created_user.is_authenticated)
        self.assertFalse(self.client.login(username=created_user.username, password=created_user.password))

    def test_validate_code_errors(self):
        payload = {"phone_number": "+375441234567", "code": "1234"}

        with self.assertNumQueries(1):
            res = self.client.post(self.validate_code_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

        authentication_code = AuthenticationCodeFactory(phone_number="+375441234567")
        payload = {"phone_number": authentication_code.phone_number, "code": "1234"}

        with self.assertNumQueries(1):
            res = self.client.post(self.validate_code_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

        authentication_code.created_at = datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(minutes=5)
        authentication_code.save()
        payload = {"phone_number": authentication_code.phone_number, "code": authentication_code.code}

        with self.assertNumQueries(1):
            res = self.client.post(self.validate_code_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

        authentication_code.created_at = datetime.datetime.now(tz=datetime.UTC)
        authentication_code.is_activated = True
        authentication_code.save()
        payload = {"phone_number": authentication_code.phone_number, "code": authentication_code.code}

        with self.assertNumQueries(1):
            res = self.client.post(self.validate_code_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_retrieve(self):
        user = UserFactory()

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(2):
            res = self.client.get(self.retrieve_url(kwargs={"username": user.username}))

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_json["username"], user.username)

    def test_send_invite_code(self):
        users = [UserFactory(invite_code=get_invite_code()) for _ in range(2)]
        payload = {"invite_code": users[0].invite_code}

        self.client.force_authenticate(user=users[1])

        with self.assertNumQueries(2):
            res = self.client.post(self.send_invite_code_url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(users[1].referral_code, users[0].invite_code)
