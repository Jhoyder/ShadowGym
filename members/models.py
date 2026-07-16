from django.db import models
from django.utils import timezone
from secrets import token_hex


# Create your models here.
class Member(models.Model):
    """Representa un miembro del gimnasio y su estado actual de membresia."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    access_code = models.CharField(max_length=16, unique=True, editable=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Estas 3 se llenan solas cuando registras un pago.
    membership_start = models.DateField(null=True, blank=True)
    membership_end = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.access_code:
            while True:
                candidate = f"SG-{token_hex(4).upper()}"
                if not Member.objects.filter(access_code=candidate).exists():
                    self.access_code = candidate
                    break
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Miembro"
        verbose_name_plural = "Miembros"


class Attendance(models.Model):
    """Marca de asistencia diaria por miembro."""

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='attendances',
    )
    date = models.DateField(default=timezone.localdate, db_index=True)
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-marked_at']
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"
        constraints = [
            models.UniqueConstraint(
                fields=['member', 'date'],
                name='unique_member_daily_attendance',
            )
        ]

    def __str__(self):
        return f"{self.member} - {self.date}"