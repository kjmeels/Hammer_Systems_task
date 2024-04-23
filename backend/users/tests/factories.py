import factory
from factory.django import DjangoModelFactory

from common.utils import get_invite_code, generate_4_symbols_code
from ..models import User, AuthenticationCode


class UserFactory(DjangoModelFactory):
    username = factory.Faker("phone_number")
    invite_code = get_invite_code()
    referral_code = ""

    class Meta:
        model = User


class AuthenticationCodeFactory(DjangoModelFactory):
    code = generate_4_symbols_code()
    phone_number = factory.Faker("phone_number")

    class Meta:
        model = AuthenticationCode
