from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    invite_code = models.CharField(verbose_name="Инвайт код", max_length=6, unique=True, default="")
    referral_code = models.CharField(verbose_name="Реферальный код", max_length=6, default="")

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

    def __str__(self):
        return f"{self.phone_number}"

    class Meta:
        verbose_name: str = "Код"
        verbose_name_plural: str = "Коды"
