from django.contrib import admin
from .models import Plan

class PlanAdmin(admin.ModelAdmin):
    """Admin para gestionar planes con vista previa de duracion en dias."""

    list_display = ['name', 'duration_label', 'duration_days', 'price']
    list_filter = ['duration_unit', 'price']
    search_fields = ['name']
    readonly_fields = ['duration_days_preview']
    fields = ['name', 'price', ('duration_value', 'duration_unit'), 'duration_days_preview', 'description']

    @admin.display(description='Duración')
    def duration_label(self, obj):
        return obj.get_duration_display_label()

    @admin.display(description='Duración en días')
    def duration_days_preview(self, obj):
        if obj is None:
            return '-'
        return obj.duration_days

    class Media:
        js = ('memberships/admin/plan_duration_preview.js',)

admin.site.register(Plan, PlanAdmin)
