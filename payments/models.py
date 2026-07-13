from django.db import models
from members.models import Member
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Payment(models.Model):
    PAYMENT_METHODS= [
      ('cash', 'Efectivo'),
      ('transfer','Transferencia'),
      ('card','Tarjeta'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    membership_start = models.DateField()
    membership_end = models.DateField()
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='cash')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.member} - ${self.amount} - {self.payment_date}"

    class Meta:
        ordering = ['-payment_date']

@receiver(post_save, sender=Payment)
def update_member_membership(sender, instance, created, **kwargs):
    if created:  # Solo cuando creas un pago nuevo
        member = instance.member
        member.membership_end = instance.membership_end
        member.membership_start = instance.membership_start
        member.is_active = True
        member.save()