from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models  import *

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(label='Telefon raqam',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Parol',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('phone_number', 'password')

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['phone_number', 'email', 'name', 'is_admin', 'is_staff', 'password1', 'password2']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = '__all__'

