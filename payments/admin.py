from django.contrib import admin
from .models import Payment
from .models import Member
from django.utils import timezone
# Register your models here.
@admin.register(Payment)
#no deje tocar membership_end
class PaymentAdmin(admin.ModelAdmin):
    """Admin para registrar pagos y mostrar vigencia calculada de membresia."""

    list_display = ['member', 'plan', 'amount', 'membership_start', 'membership_end', 'method']
    list_filter = ['method', 'plan', 'payment_date']
    search_fields = ['member_first_name', 'member_last_name']
    readonly_fields = ['membership_end', 'payment_date']
    
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