from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name: str = "Пользователь"
        verbose_name_plural: str = "Пользователи"


class AuthenticationCode(models.Model):
    phone_number = PhoneNumberField(verbose_name="Номер телефона", max_length=13)
    code = models.CharField(verbose_name="Код", max_length=4)
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    is_activated = models.BooleanField(verbose_name="Активирован", default=False)
