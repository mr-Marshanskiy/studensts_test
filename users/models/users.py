from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as AuthGroup
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from users.constants import DIRECTOR_GROUP
from users.managers import CustomUserManager


class Group(AuthGroup):
    code = models.CharField('Code', max_length=32, null=True, unique=True)


class User(AbstractUser):
    username = models.CharField(
        'Username', max_length=64, unique=True, null=True, blank=True
    )
    email = models.EmailField('Email', unique=True, null=True, blank=True)
    phone_number = PhoneNumberField('Phone', unique=True, null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()
    groups = models.ManyToManyField(
        Group, related_name='groups', verbose_name='Groups', blank=True
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_director(self):
        return self.groups.filter(code=DIRECTOR_GROUP).exists()

    def __str__(self):
        return f'{self.full_name} ({self.pk})'
