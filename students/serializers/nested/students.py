from django.contrib.auth import get_user_model

from common.serializers.mixins import InfoModelSerializer
from students.models.students import Student

User = get_user_model()


class StudentShortSerializer(InfoModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
