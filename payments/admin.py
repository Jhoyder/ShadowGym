from django.contrib import admin
from .models import Payment
from django.utils import timezone
# Register your models here.
@admin.register(Payment)
#no deje tocar membership_end
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['member', 'plan', 'amount', 'membership_start', 'membership_end', 'method']
    list_filter = ['method', 'plan', 'payment_date']
    search_fields = ['member__first_name', 'member__last_name']
    readonly_fields = ['membership_end', 'payment_date']
    autocomplete_fields = ['member', 'plan']
    
    fieldsets = (
        ('Datos del Pago', {
            'fields': ('member', 'plan', 'amount', 'method')
        }),
        ('Vigencia', {
            'fields': ('membership_start', 'membership_end')
        }),
        ('Otros', {
            'fields': ('notes', 'payment_date')
        }),
    )
    admin.site.register(Payment)