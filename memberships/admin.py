from django.contrib import admin
from .models import MembershipPlan
# Register your models here.
@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration', 'duration_unit', 'price', 'is_active']
    list_filter = ['is_active', 'duration_unit']
    search_fields = ['name']
    list_editable = ['price', 'is_active']