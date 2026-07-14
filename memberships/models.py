from django.db import models

# Create your models here
class MembershipPlan(models.Model):
    DURATION_CHOICES = [
        ('days', 'Días'),
        ('months', 'Meses'),
        ('years', 'Años'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nombre del Plan")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Precio")
    duration = models.IntegerField(verbose_name="Duración")
    duration_unit = models.CharField(max_length=10, choices=DURATION_CHOICES, default='months', verbose_name="Unidad")
    duration_type = models.CharField(
        max_length=10, 
        choices=DURATION_CHOICES, 
        default='meses',
        verbose_name="Tipo de Duración"
    )
    is_active = models.BooleanField(default=True, verbose_name="Plan Activo")
    
    def __str__(self):
        return f"{self.name} - {self.duration} {self.get_duration_unit_display()}- ${self.price}"
    
    class Meta:
        verbose_name = "Plan de Membresía"
        verbose_name_plural = "Planes de Membresía"
        ordering = ['price']