from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    role_choices = (
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
        (USER, USER),
    )
    email = models.EmailField(blank=True, unique=True)
    role = models.CharField(max_length=10, choices=role_choices, default=USER)
    bio = models.TextField(null=True)
    password = models.CharField(max_length=128, null=True)
    confirmation_code = models.CharField(max_length=200, null=True, blank=True)

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
