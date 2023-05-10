import django_filters
from django.db.models import Q

from students.models import sections, students


class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = students.Student
        fields = ('whatsapp_available', )


class SectionFilter(django_filters.FilterSet):
    has_no_email = django_filters.BooleanFilter(method='has_no_email_filter', )
    has_no_phone = django_filters.BooleanFilter(method='has_no_phone_filter', )

    class Meta:
        model = sections.Section
        fields = {
            'created_at': ['exact', 'gte', 'gt', 'lte', 'lt'],
            'tutor': ['exact'],
        }

    def has_no_email_filter(self, queryset, name, value):
        query = Q(members_without_email__gt=0)
        return self._filter_bool_by_query(queryset, query, value)

    def has_no_phone_filter(self, queryset, name, value):
        query = Q(members_without_phone__gt=0)
        return self._filter_bool_by_query(queryset, query, value)

    def _filter_bool_by_query(self, queryset, query, value):
        if value:
            return queryset.filter(query)
        else:
            return queryset.exclude(query)
