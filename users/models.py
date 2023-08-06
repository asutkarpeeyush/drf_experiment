from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from .managers import DRFUserManager
from django.utils import timezone

class DRFUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email address", unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = DRFUserManager()

    def __str__(self):
        return self.email
