import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from common.serializers.mixins import (ExtendedModelSerializer,
                                       InfoModelSerializer,)
from students.models.students import Student

User = get_user_model()


class StudentListSerializer(InfoModelSerializer):
    age = serializers.IntegerField()
    section_count = serializers.IntegerField()

    class Meta:
        model = Student
        fields = '__all__'


class StudentRetrieveSerializer(StudentListSerializer):

    class Meta:
        model = Student
        fields = '__all__'


class StudentCreateUpdateCommonSerializer(ExtendedModelSerializer):
    class Meta:
        abstract = True

    def validate_dob(self, value):
        if not value:
            return value
        now = datetime.date.today()
        if now - value > datetime.timedelta(days=365 * 100):
            raise ParseError(
                'Enter a valid day of birth.'
            )
        if now - value < datetime.timedelta(days=365 * 10):
            raise ParseError(
                'Your age is too short.'
            )
        return value


class StudentCreateSerializer(StudentCreateUpdateCommonSerializer):

    class Meta:
        model = Student
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def validate_name(self, value):
        if self.Meta.model.objects.filter(name=value).exists():
            raise ParseError('Student with this name already exists')
        return value


class StudentUpdateSerializer(StudentCreateUpdateCommonSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def validate_name(self, value):
        if self.Meta.model.objects.filter(
            name=value
        ).exclude(pk=self.instance.pk).exists():
            raise ParseError('Student with this name already exists')
        return value
