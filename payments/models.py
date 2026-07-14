from django.db import models
from members.models import Member
from memberships.models import MembershipPlan
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta

# Create your models here.
class Payment(models.Model):
    PAYMENT_METHODS= [
      ('cash', 'Efectivo'),
      ('transfer','Transferencia'),
      ('card','Tarjeta'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='payments')
    plan = models.ForeignKey(MembershipPlan, on_delete=models.PROTECT, verbose_name="Plan")
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    membership_start = models.DateField()
    membership_end = models.DateField()
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='cash')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-payment_date']
   
    def __str__(self):
        return f"{self.member} - {self.plan.name} -${self.amount}"

@receiver(post_save, sender=Payment)

def calculate_end_date(sender, instance, **kwargs):
    if instance.membership_start and instance.plan:
        if instance.plan.duration_unit == 'days':
            instance.membership_end = instance.membership_start + relativedelta(days=instance.plan.duration)
        elif instance.plan.duration_unit == 'months':
            instance.membership_end = instance.membership_start + relativedelta(months=instance.plan.duration)
        elif instance.plan.duration_unit == 'years':
            instance.membership_end = instance.membership_start + relativedelta(years=instance.plan.duration)
