from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from common.models.mixins import InfoMixin

User = get_user_model()


class Section(InfoMixin):
    name = models.CharField('Name', max_length=255, unique=True)
    tutor = models.ForeignKey(User, models.RESTRICT, 'sections')
    direction = models.ForeignKey(
        'Direction', models.RESTRICT, 'sections',
        verbose_name='Direction',
    )
    members = models.ManyToManyField(
        'Student', 'section_members', verbose_name='Members',
        blank=True, through='Member',
    )

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'
        ordering = ('name', 'id',)

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Member(models.Model):
    section = models.ForeignKey(
        'Section', models.CASCADE, 'members_info',
    )
    student = models.ForeignKey(
        'Student', models.CASCADE, 'sections_info',
    )
    date_joined = models.DateField('Date joined', default=timezone.now)

    class Meta:
        verbose_name = 'Section Member'
        verbose_name_plural = 'Section Members'
        ordering = ('-date_joined',)
        unique_together = (('section', 'student'),)

    def __str__(self):
        return f'Member #{self.pk} {self.student}'
