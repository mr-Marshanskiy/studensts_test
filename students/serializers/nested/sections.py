from django.contrib.auth import get_user_model

from common.serializers.mixins import (ExtendedModelSerializer,
                                       InfoModelSerializer)
from students.models.sections import Member
from students.serializers.nested.students import StudentShortSerializer
from users.serializers.nested.users import UserShortSerializer

User = get_user_model()


class SectionMemberShortSerializer(ExtendedModelSerializer):
    student = StudentShortSerializer()

    class Meta:
        model = Member
        fields = (
            'id',
            'student',
            'date_joined',
        )


class SectionShortSerializer(InfoModelSerializer):
    tutor = UserShortSerializer()

    class Meta:
        model = Member
        fields = (
            'id',
            'tutor',
            'name',
            'created_at',
        )
