from django.contrib.admin import register, ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, AuthenticationCode


@register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password", "invite_code", "referral_code")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


@register(AuthenticationCode)
class AuthenticationCodeAdmin(ModelAdmin):
    list_display = ("phone_number", "code", "is_activated",)
