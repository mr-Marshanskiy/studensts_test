from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter, SearchFilter

from common.views.mixins import LCRUDViewSet
from students.backends import MySections
from students.filters import SectionFilter
from students.models import sections
from students.permissions import IsTutor, IsDirectorOrSuperuser
from students.serializers.api import sections as sections_s


@extend_schema_view(
    list=extend_schema(summary='List sections', tags=['Sections']),
    retrieve=extend_schema(summary='Retrieve sections', tags=['Sections']),
    create=extend_schema(summary='Create section', tags=['Sections']),
    update=extend_schema(summary='Update section', tags=['Sections']),
    partial_update=extend_schema(summary='Partial update section', tags=['Sections']),
    destroy=extend_schema(summary='Destroy section', tags=['Sections']),
)
class SectionView(LCRUDViewSet):
    queryset = sections.Section.objects.all()
    serializer_class = sections_s.SectionListSerializer

    multi_permission_classes = {
        'list': [IsTutor | IsDirectorOrSuperuser],
        'retrieve': [IsTutor | IsDirectorOrSuperuser],
        'create': [IsDirectorOrSuperuser],
        'partial_update': [IsDirectorOrSuperuser],
        'destroy': [IsDirectorOrSuperuser],
    }
    multi_serializer_class = {
        'list': sections_s.SectionListSerializer,
        'retrieve': sections_s.SectionRetrieveSerializer,
        'create': sections_s.SectionCreateSerializer,
        'partial_update': sections_s.SectionUpdateSerializer,
    }

    http_method_names = ('get', 'post', 'patch', 'delete')

    filter_backends = (
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
        MySections,
    )
    filterset_class = SectionFilter
    ordering = ('name', 'id',)

    def get_queryset(self):
        queryset = (
            sections.Section.objects
            .select_related(
                'tutor',
                'direction',
            )
            .prefetch_related(
                'members',
                'members_info',
            )
            .annotate(
                pax=Count('members', distinct=True),
                members_without_email=Count(
                    'members', filter=Q(members__email__isnull=True), distinct=True
                ),
                members_without_phone=Count(
                    'members', filter=Q(members__phone__isnull=True), distinct=True
                ),
            )
        )
        return queryset
