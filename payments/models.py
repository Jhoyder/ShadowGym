from django.db import models
from members.models import Member
from memberships.models import Plan
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Payment(models.Model):
    """Registra un pago y la vigencia de membresia asociada al miembro."""

    PAYMENT_METHODS = [
        ('cash', 'Efectivo'),
        ('transfer', 'Transferencia'),
        ('card', 'Tarjeta'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='payments')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, verbose_name="Plan")
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    membership_start = models.DateField()
    membership_end = models.DateField()
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='cash')
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.member} - {self.plan.name if self.plan else 'Sin plan'} -${self.amount}"
    
    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-payment_date']
   
    def save(self, *args, **kwargs):
        """Calcula automáticamente la fecha de fin basada en el plan seleccionado"""
        if self.plan and self.membership_start:
            # Sumar los días del plan a la fecha de inicio
            self.membership_end = self.membership_start + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

@receiver(post_save, sender=Payment)

def update_member_membership(sender, instance, created, **kwargs):
    """Actualiza fechas y estado del miembro cuando se crea un nuevo pago."""
    if created:  # Solo cuando creas un pago nuevo
        member = instance.member
        member.membership_end = instance.membership_end
        member.membership_start = instance.membership_start
        member.is_active = True
        member.save()