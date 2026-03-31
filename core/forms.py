from django import forms
from .models import SupportTicket

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['subject', 'category', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0 py-2',
                'placeholder': 'Briefly describe your issue'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select bg-light border-0 py-2'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control bg-light border-0',
                'rows': 5,
                'placeholder': 'Provide details about your problem...'
            }),
        }
