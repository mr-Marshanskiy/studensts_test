from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action

from common.views.mixins import LCDViewSet
from students.backends import SectionMember
from students.models.sections import Member
from students.permissions import IsTutor
from students.serializers.api import members as members_s


@extend_schema_view(
    list=extend_schema(summary='List members', tags=['Sections: Members']),
    create=extend_schema(summary='Create member', tags=['Sections: Members']),
    destroy=extend_schema(summary='Destroy member', tags=['Sections: Members']),
    search=extend_schema(filters=True, summary='Brief list members for search', tags=['Sections: Dicts']),
)
class MemberView(LCDViewSet):
    permission_classes = [IsTutor]

    queryset = Member.objects.all()
    serializer_class = members_s.MemberListSerializer

    multi_serializer_class = {
        'list': members_s.MemberListSerializer,
        'create': members_s.MemberCreateSerializer,
        'search': members_s.MemberSearchSerializer,
    }

    lookup_url_kwarg = 'member_id'

    filter_backends = (SectionMember,)

    def get_queryset(self):
        qs = Member.objects.select_related(
            'student',
        )
        return qs

    @action(methods=['GET'], detail=False, url_path='search')
    def search(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
