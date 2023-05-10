from crum import get_current_user
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from common.serializers.mixins import ExtendedModelSerializer
from students.models.sections import Member, Section
from students.serializers.nested.sections import SectionShortSerializer
from students.serializers.nested.students import StudentShortSerializer

User = get_user_model()


class MemberSearchSerializer(ExtendedModelSerializer):
    full_name = serializers.CharField(source='student.full_name')

    class Meta:
        model = Member
        fields = (
            'id',
            'full_name',
            'date_joined',
        )


class MemberListSerializer(ExtendedModelSerializer):
    student = StudentShortSerializer()

    class Meta:
        model = Member
        fields = (
            'id',
            'student',
            'date_joined',
        )


class MemberRetrieveSerializer(MemberListSerializer):
    section = SectionShortSerializer()

    class Meta:
        model = Member
        fields = '__all__'


class MemberCreateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Member
        fields = (
            'id',
            'student',
        )

    def validate(self, attrs):
        section = self.get_object_from_url(Section)
        if not section:
            raise ParseError('Invalid section.')

        if section.tutor != get_current_user():
            raise ParseError(
                'You are not allowed to create members of this section.'
            )

        if attrs['student'] in section.members.all():
            raise ParseError(
                'This student is already a member of this section.'
            )
        attrs['section'] = section
        return attrs
