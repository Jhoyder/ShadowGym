from django.contrib import admin
from .models import MembershipPlan
# Register your models here.
@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'duration_type', 'is_active']
    list_editable = ['price', 'is_active']
    list_filter = ['is_active']