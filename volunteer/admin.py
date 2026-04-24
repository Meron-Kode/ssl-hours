from django.contrib import admin
from .models import VolunteerLog


@admin.register(VolunteerLog)
class VolunteerLogAdmin(admin.ModelAdmin):
    list_display = ('student', 'organization_name', 'volunteer_date', 'hours_worked', 'status', 'created_at')
    list_filter = ('status', 'volunteer_date')
    search_fields = ('student__username', 'organization_name', 'supervisor_name')
    list_editable = ('status',)
