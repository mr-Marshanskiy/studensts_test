import datetime

from django.db.models import Count, F, Func
from django.db.models.functions import ExtractYear
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter, SearchFilter

from common.views.mixins import LCRUDViewSet
from students.backends import MySections
from students.filters import StudentFilter
from students.models import students
from students.permissions import (IsDirectorOrSuperuser, IsStudentCreator,
                                  IsTutor)
from students.serializers.api import students as students_s


@extend_schema_view(
    list=extend_schema(summary='List students', tags=['Students']),
    retrieve=extend_schema(summary='Retrieve student', tags=['Students']),
    create=extend_schema(summary='Create student', tags=['Students']),
    partial_update=extend_schema(summary='Partial update student', tags=['Students']),
    destroy=extend_schema(summary='Destroy student', tags=['Students']),
)
class StudentView(LCRUDViewSet):
    queryset = students.Student.objects.all()
    serializer_class = students_s.StudentListSerializer

    multi_permission_classes = {
        'list': [IsTutor | IsDirectorOrSuperuser],
        'retrieve': [IsTutor | IsDirectorOrSuperuser],
        'create': [IsStudentCreator],
        'partial_update': [IsStudentCreator],
        'destroy': [IsStudentCreator],
    }
    multi_serializer_class = {
        'list': students_s.StudentListSerializer,
        'retrieve': students_s.StudentRetrieveSerializer,
        'create': students_s.StudentCreateSerializer,
        'partial_update': students_s.StudentUpdateSerializer,
    }

    http_method_names = ('get', 'post', 'patch', 'delete')

    filter_backends = (
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
        MySections,
    )
    filterset_class = StudentFilter
    ordering = ('first_name', 'last_name', 'id',)

    def get_queryset(self):
        now = datetime.datetime.now().date()
        queryset = (
            students.Student.objects
            .prefetch_related(
                'created_by',
                'updated_by',
            )
            .annotate(
                section_count=Count('section_members', distinct=True),
                age=(ExtractYear(Func(now, F('dob'), function='age'))),
            )
        )
        return queryset
