from django import forms
from .models import RSVPResponse

class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVPResponse
        fields = ['name', 'attendance', 'drinks']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Иван Иванов'
            }),
            'attendance': forms.RadioSelect(),
            'drinks': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'name': 'Ваше имя и фамилия',
            'attendance': 'Будете ли вы на мероприятии?',
            'drinks': 'Если пьёте, то что:',
        }