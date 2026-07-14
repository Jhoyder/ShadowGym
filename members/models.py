from django.db import models

class Plan(models.Model):
    """Modelo para los planes de membresía"""
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration_days = models.IntegerField()  # Duración en días
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.duration_days} Días - ${self.price}"
    
    class Meta:
        ordering = ['name']
        verbose_name = "Plan"
        verbose_name_plural = "Planes"


class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Estas 3 se llenan solas cuando registras un pago
    membership_start = models.DateField(null=True, blank=True)
    membership_end = models.DateField(null=True, blank=True) 
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = "Miembro"
        verbose_name_plural = "Miembros"
