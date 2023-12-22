"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    '''Manager for users.'''
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email, and password."""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'