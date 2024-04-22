# from functools import partial
#
# from django.contrib.auth.hashers import make_password
# from pytest import mark
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
#
# from users.models import User
# from users.tests.factories import UserFactory
#
#
# @mark.django_db
# class TestUserViewSet(APITestCase):
#     def setUp(self):
#         self.list_url: str = reverse("users-list")
#         self.change_password_url: str = reverse("users-change-password")
#         self.reset_password_url: str = reverse("users-reset-password")
#         self.login_url: str = reverse("users-login")
#
#     def test_create(self):
#         payload = {"email": "user@example.com", "password": "user"}
#
#         with self.assertNumQueries(2):
#             res = self.client.post(self.list_url, data=payload)
#
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(User.objects.count(), 1)
#
#     def test_change_password(self):
#         user = UserFactory()
#         user.set_password("user")
#         user.save()
#         old_password = "user"
#         new_password = "admin"
#
#         payload = {
#             "old_password": old_password,
#             "new_password": new_password,
#         }
#
#         self.client.force_authenticate(user=user)
#
#         with self.assertNumQueries(1):
#             res = self.client.post(self.change_password_url, data=payload)
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#
#         user.refresh_from_db()
#         self.assertFalse(self.client.login(email=user.email, password=old_password))
#         self.assertTrue(self.client.login(email=user.email, password=new_password))
#
#     def reset_password(self):
#         user = UserFactory()
#         password = "user"
#         user.set_password(password)
#         user.save()
#         self.client.force_authenticate(user=user)
#
#         with self.assertNumQueries(1):
#             res = self.client.post(self.reset_password_url)
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#
#         user.refresh_from_db()
#         self.assertFalse(self.client.login(email=user.email, password=password))
#         self.assertTrue(self.client.login(email=user.email, password="1111"))
#
#     def test_login(self):
#         user = UserFactory(email="user@example.com")
#         password = "user"
#         user.set_password(password)
#         user.save()
#
#         with self.assertNumQueries(2):
#             res = self.client.post(self.login_url, data={"email": user.email, "password": password})
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertTrue(user.is_authenticated)
