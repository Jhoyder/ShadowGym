from django import forms

from .models import Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'first_name',
            'last_name',
            'id_number',
            'phone',
            'email',
            'membership_start',
            'membership_end',
            'is_active',
        ]
        widgets = {
            'membership_start': forms.DateInput(attrs={'type': 'date', 'class': 'date-field'}),
            'membership_end': forms.DateInput(attrs={'type': 'date', 'class': 'date-field'}),
        }
        labels = {
            'membership_start': 'Inicio de membresía',
            'membership_end': 'Fin de membresía',
            'is_active': 'Activo',
        }


class AttendanceCodeForm(forms.Form):
    code = forms.CharField(
        max_length=32,
        label='Codigo de acceso',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ej: SG-AB12CD34 o cedula',
                'autocomplete': 'off',
            }
        ),
    )

    def clean_code(self):
        return self.cleaned_data['code'].strip().upper()
