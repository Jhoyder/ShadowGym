from django.contrib import admin
from .models import Member

class MemberAdmin(admin.ModelAdmin):
    """Configuracion del admin para listar y buscar miembros."""

    list_display = ['first_name', 'last_name', 'id_number', 'phone', 'is_active', 'membership_start', 'membership_end']
    list_filter = ['is_active', 'membership_start', 'membership_end']
    search_fields = ['first_name', 'last_name', 'id_number', 'phone']
    readonly_fields = ['created_at']

admin.site.register(Member, MemberAdmin)
