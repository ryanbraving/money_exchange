import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from django.utils.translation import gettext_lazy as _

# from .managers import CustomUserManager

class User(AbstractUser):
    # username = None
    uuid = models.CharField(max_length=8, default=uuid.uuid4, editable=False, unique=True)

    # email = models.EmailField(_('email address'), unique=True)
    username = models.EmailField(_('email address'), unique=True, null=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    # REQUIRED_FIELDS = ["uuid"]
    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []

    # objects = UserManager()

    def save(self, *args, **kwargs):
        self.uuid = str(self.uuid).split("-")[0]
        super(User, self).save(*args, **kwargs)
