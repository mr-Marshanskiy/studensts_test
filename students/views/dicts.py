from drf_spectacular.utils import extend_schema, extend_schema_view

from common.views.mixins import DictListMixin
from students.models import dicts


@extend_schema_view(
    list=extend_schema(summary='List directions', tags=['Sections: Dicts']),
)
class DirectionView(DictListMixin):
    model = dicts.Direction
