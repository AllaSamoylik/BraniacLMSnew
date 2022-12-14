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
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. ASCII letters and digits only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    age = models.PositiveSmallIntegerField(**NULLABLE)
    avatar = models.ImageField(upload_to=users_avatars_path, **NULLABLE)
    email = models.EmailField(
        _("email address"),
        max_length=256,
        unique=True,
        error_messages={
            "unique": _("A user with that email address already exists."),
        },
    )
