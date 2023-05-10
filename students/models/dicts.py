from django.contrib.auth import get_user_model

from common.models.mixins import BaseDictModelMixin

User = get_user_model()


class Direction(BaseDictModelMixin):

    class Meta:
        verbose_name = 'Direction'
        verbose_name_plural = 'Directions'
