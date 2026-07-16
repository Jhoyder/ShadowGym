from django import forms

from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'member',
            'plan',
            'amount',
            'membership_start',
            'method',
            'notes',
        ]
        widgets = {
            'membership_start': forms.DateInput(attrs={'type': 'date', 'class': 'date-field'}),
        }
        labels = {
            'membership_start': 'Inicio de membresía',
        }
