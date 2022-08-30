from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from mainapp.models import NULLABLE

from pathlib import Path
from time import time


def users_avatars_path(instance, filename):
    # file will be uploaded to
    #   MEDIA_ROOT / user_<username> / avatars / <filename>
    num = int(time() * 1000)
    suff = Path(filename).suffix
    return "user_{0}/avatars/{1}".format(instance.username, f"pic_{num}{suff}")


class CustomUser(AbstractUser):
    username_validator = ASCIIUsernameValidator()
    age = models.PositiveSmallIntegerField(**NULLABLE)
    avatar = models.ImageField(upload_to=users_avatars_path, **NULLABLE)
    email = models.EmailField(
        _("email address"),
        max_length=256,
        # Флаг уникальности отключён для проверки разных способов логина (везде одна почта:)C
        # unique=True,
        error_messages={
            "unique": _("A user with that email address already exists."),
        },
    )
