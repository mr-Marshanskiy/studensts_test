from django.contrib import admin

from students.models import students


@admin.register(students.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'phone', )
    list_display_links = ('id', 'full_name',)
    search_fields = ('first_name', 'last_name', 'email', 'phone',)
    readonly_fields = (
        'created_at', 'created_by', 'updated_at', 'updated_by',
    )
