from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control bg-light border-0', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control bg-light border-0', 'placeholder': 'Last Name'}))
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update field order or widgets if needed
        self.fields['email'].required = True
        self.fields['username'].required = False # We will auto-generate it if missing

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg bg-light border-0',
        'placeholder': 'email or mobile',
        'id': 'email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg bg-light border-0',
        'placeholder': 'Password',
        'id': 'password'
    }))

class OTPForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg bg-light border-0',
            'placeholder': 'Enter your registered email'
        })
    )

class OTPVerifyForm(forms.Form):
    otp_code = forms.CharField(
        max_length=6, 
        label="OTP Code",
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center fw-bold fs-4 border-2',
            'placeholder': 'Enter 6-digit OTP',
            'maxlength': '6'
        })
    )

class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg bg-light border-0',
            'placeholder': 'Enter new password'
        }),
        label="New Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg bg-light border-0',
            'placeholder': 'Confirm new password'
        }),
        label="Confirm Password",
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
