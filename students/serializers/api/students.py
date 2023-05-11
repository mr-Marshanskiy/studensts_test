import datetime

from django.contrib.auth import get_user_model
from django.db.models.functions import Lower
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from common.serializers.mixins import (ExtendedModelSerializer,
                                       InfoModelSerializer)
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

    def validate_email(self, value):
        if not value:
            return value

        same_email_qs = self.Meta.model.objects.annotate(
            lower_email=Lower('email')
        ).filter(lower_email=value.lower())

        if self.instance:
            same_email_qs = same_email_qs.exclude(pk=self.instance.pk)

        if same_email_qs.exists():
            raise ParseError('Your email address is already in use.')

        # Чтобы 100% в БД сохранялись в нижнем регистре
        # p.s можно ещё кастомное поле на основе EmailField определить, чтобы
        # в админке тоже сохранялись в нижнем регистре
        return value.lower()

    def validate_full_name_unique(self, attrs):
        first_name = attrs.get('first_name') or self._get_current_value('first_name')
        last_name = attrs.get('last_name') or self._get_current_value('last_name')
        middle_name = attrs.get('middle_name') or self._get_current_value('middle_name')

        # Выборка будет зависеть от конкетных условий в т.ч. что делать, если
        # отсутствует Middle name. В данном случае самый топорный вариант

        # p.s. можно запариться и так же, как и в случае с проверкой email
        # приводить в нижний регистр
        same_full_name_qs = self.Meta.model.objects.filter(
            first_name=first_name, last_name=last_name, middle_name=middle_name
        )
        if self.instance:
            same_full_name_qs = same_full_name_qs.exclude(pk=self.instance.pk)

        if same_full_name_qs.exists():
            raise ParseError(
                'Student with this full name already exists.'
            )
        return

    def _get_current_value(self, attr_name):
        return getattr(self.instance, attr_name) if self.instance else None


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

    def validate(self, attrs):
        self.validate_full_name_unique(attrs)
        return attrs


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

    def validate(self, attrs):
        self.validate_full_name_unique(attrs)
        return attrs
