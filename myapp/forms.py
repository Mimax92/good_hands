from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

def validate_email(value):
    if get_user_model().objects.filter(email=value).exists():
        raise ValidationError('Email already exists')

class CreateUserForm(forms.Form):
    first_name = forms.CharField(max_length=64, label='first_name', widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(max_length=64, label='last_name', widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.EmailField(validators=[EmailValidator(), validate_email], label='email', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}), label='password')
    repeated_password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}), label='repeated_password')


class UserChangeForm(UserChangeForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

        def clean(self):
            cleaned_data = super(UserChangeForm, self).clean()
            password = cleaned_data.get("password")
            confirm_password = cleaned_data.get("confirm_password")

            if password != confirm_password:
                self.add_error('confirm_password', "Password does not match")

            return cleaned_data

class ContactFormEmail(forms.Form):
    fromemail = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(required=True)