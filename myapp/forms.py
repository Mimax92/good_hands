from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model


def validate_email(value):
    if get_user_model().objects.filter(email=value).exists():
        raise ValidationError('Email already exists')

class CreateUserForm(forms.Form):
    first_name = forms.CharField(max_length=64, label='first_name', widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(max_length=64, label='last_name', widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.EmailField(validators=[EmailValidator(), validate_email], label='email', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}), label='password')
    repeated_password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}), label='repeated_password')
