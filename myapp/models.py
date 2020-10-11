from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager


USER_TYPE_CHOICES = (
    ('admin', 'ADMIN'),
    ('basic_user', 'BASIC_USER'),
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email address'), unique=True)
    user_type = models.CharField(_('User type'), max_length=11, choices=USER_TYPE_CHOICES, default='basic_user')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Producer(models.Model):
    name = models.CharField(_('Name'), max_length=30, unique=True)

    REQUIRED_FIELDS = ['name']

    objects = models.Manager()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(_('Name'), max_length=30)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    price = models.FloatField(default=10)
    discounted_price = models.FloatField(null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['name', 'producer', 'price', 'is_active']

    objects = models.Manager()

    def __str__(self):
        return self.producer.name
