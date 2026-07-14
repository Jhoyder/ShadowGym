from django.contrib import admin
from .models import Member, Plan

class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration_days', 'price']
    list_filter = ['duration_days', 'price']
    search_fields = ['name']

class MemberAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'id_number', 'phone', 'is_active', 'membership_start', 'membership_end']
    list_filter = ['is_active', 'membership_start', 'membership_end']
    search_fields = ['first_name', 'last_name', 'id_number', 'phone']
    readonly_fields = ['created_at']

admin.site.register(Plan, PlanAdmin)
admin.site.register(Member, MemberAdmin)
