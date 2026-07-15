from django.db import models
from django.core.validators import MinValueValidator


class Plan(models.Model):
    """Define un plan de membresia con duracion configurable y precio."""

    DAYS = 'days'
    MONTHS = 'months'
    YEARS = 'years'

    DURATION_UNIT_CHOICES = [
        (DAYS, 'Días'),
        (MONTHS, 'Meses'),
        (YEARS, 'Años'),
    ]

    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])
    duration_value = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='Duración')
    duration_unit = models.CharField(max_length=10, choices=DURATION_UNIT_CHOICES, default=MONTHS, verbose_name='Unidad')
    duration_days = models.PositiveIntegerField(editable=False)
    description = models.TextField(blank=True, null=True)

    def to_days(self):
        """Convierte la duracion ingresada (dias/meses/anios) a dias."""
        if self.duration_unit == self.DAYS:
            return self.duration_value
        if self.duration_unit == self.MONTHS:
            return self.duration_value * 30
        if self.duration_unit == self.YEARS:
            return self.duration_value * 365
        return self.duration_value

    def get_duration_display_label(self):
        """Devuelve una etiqueta legible para mostrar la duracion elegida."""
        unit_labels = {
            self.DAYS: 'día' if self.duration_value == 1 else 'días',
            self.MONTHS: 'mes' if self.duration_value == 1 else 'meses',
            self.YEARS: 'año' if self.duration_value == 1 else 'años',
        }
        return f"{self.duration_value} {unit_labels.get(self.duration_unit, 'días')}"

    def save(self, *args, **kwargs):
        """Sincroniza duration_days antes de guardar el plan."""
        self.duration_days = self.to_days()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.get_duration_display_label()} - ${self.price}"
   
    class Meta:
        ordering = ['name']
        verbose_name = "Plan"
        verbose_name_plural = "Planes"