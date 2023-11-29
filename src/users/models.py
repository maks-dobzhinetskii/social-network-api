from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, verbose_name='Email')
    phone = PhoneNumberField(blank=True, null=True, unique=True, verbose_name='Phone')
    last_request = models.DateTimeField(null=True, blank=True, verbose_name='Last Request')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
