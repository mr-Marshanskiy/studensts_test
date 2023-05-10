from django.contrib import admin
from django.db.models import Count

from students.models import sections, dicts


class MemberInline(admin.TabularInline):
    model = sections.Member
    fields = ('student', 'date_joined',)


@admin.register(dicts.Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'color',)


@admin.register(sections.Section)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tutor', 'pax',)
    autocomplete_fields = ('tutor',)
    inlines = (MemberInline,)
    readonly_fields = (
        'created_at', 'created_by', 'updated_at', 'updated_by',
    )

    def pax(self, obj):
        return obj.pax

    pax.field_name = 'Pax'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            pax=Count('members')
        )