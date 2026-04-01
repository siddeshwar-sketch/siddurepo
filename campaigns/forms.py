from django import forms
from .models import Campaign, CampaignProof, Category


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ('title', 'description', 'goal_amount', 'category', 'location', 'image', 'bank_name', 'bank_account_number', 'ifsc_code')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe why you are raising funds...'}),
            'goal_amount': forms.NumberInput(attrs={'min': '1', 'step': '0.01', 'placeholder': 'Enter target goal'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter campaign location'}),
            'bank_name': forms.TextInput(attrs={'placeholder': 'e.g. State Bank of India', 'required': 'required'}),
            'bank_account_number': forms.TextInput(attrs={'placeholder': 'Enter Account Number', 'required': 'required'}),
            'ifsc_code': forms.TextInput(attrs={'placeholder': 'Enter IFSC Code', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.exclude(slug='medical-emergency').order_by('id')
        self.fields['category'].empty_label = 'Select Category'
        self.fields['goal_amount'].widget.attrs.setdefault('autocomplete', 'off')
        self.fields['location'].widget.attrs.setdefault('autocomplete', 'off')
        
        # Make bank details mandatory
        self.fields['bank_name'].required = True
        self.fields['bank_account_number'].required = True
        self.fields['ifsc_code'].required = True


class CampaignProofForm(forms.ModelForm):
    class Meta:
        model = CampaignProof
        fields = ('document', 'document_type', 'description')
