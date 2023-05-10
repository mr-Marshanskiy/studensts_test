from crum import get_current_user
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from common.serializers.mixins import (ExtendedModelSerializer,
                                       InfoModelSerializer, DictMixinSerializer)
from students.models.sections import Section
from students.serializers.nested.sections import SectionMemberShortSerializer
from users.serializers.nested.users import UserShortSerializer

User = get_user_model()


class SectionListSerializer(InfoModelSerializer):
    tutor = UserShortSerializer()
    direction = DictMixinSerializer()
    members = SectionMemberShortSerializer(source='members_info', many=True)
    pax = serializers.IntegerField()
    members_without_email = serializers.IntegerField()
    members_without_phone = serializers.IntegerField()

    class Meta:
        model = Section
        fields = (
            'id',
            'name',
            'tutor',
            'direction',
            'members',
            'pax',
            'members_without_email',
            'members_without_phone',
            'created_at',
        )


class SectionRetrieveSerializer(SectionListSerializer):

    class Meta:
        model = Section
        fields = '__all__'


class SectionCreateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Section
        fields = (
            'id',
            'name',
            'tutor',
            'direction',
        )

    def validate_name(self, value):
        if self.Meta.model.objects.filter(name=value).exists():
            raise ParseError(
                'Section with this name already exists'
            )
        return value


class SectionUpdateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Section
        fields = (
            'id',
            'direction',
        )

    def validate_name(self, value):
        if self.Meta.model.objects.filter(
            name=value
        ).exclude(pk=self.instance.pk).exists():
            raise ParseError('Section with this name already exists')
        return value
