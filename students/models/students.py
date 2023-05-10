from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from common.models.mixins import InfoMixin


class Student(InfoMixin):
    first_name = models.CharField('First name', max_length=31)
    last_name = models.CharField('Last name', max_length=63)
    middle_name = models.CharField(
        'Middle name', max_length=63, null=True, blank=True
    )
    dob = models.DateField('Birthday', null=True, blank=True)
    email = models.EmailField('Email', null=True, blank=True)
    phone = PhoneNumberField('Phone Number', null=True, blank=True)
    whatsapp_available = models.BooleanField(
        'Whatsaspp available', default=False
    )

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    @property
    def full_name(self):
        fields = (self.first_name, self.middle_name, self.last_name)
        return ' '.join([field for field in fields if field])

    def __str__(self):
        return f'{self.full_name} ({self.pk})'
