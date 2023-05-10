from rest_framework.filters import BaseFilterBackend


class MySections(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        if user.is_superuser or user.is_director:
            return queryset
        return queryset.filter(tutor=user)


class SectionMember(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        section_id = request.parser_context['kwargs'].get('pk')
        queryset = queryset.filter(section_id=section_id,)

        user = request.user
        if user.is_superuser or user.is_director:
            return queryset
        return queryset.filter(section__tutor=user)
