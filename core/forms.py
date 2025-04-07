from django.forms import ModelForm
from django import forms
from .models import users, transaction
from django.forms.widgets import PasswordInput, TextInput, NumberInput, Select

class RegisterForm(ModelForm):
    class Meta:
        model = users
        fields = ['username', 'password', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email', 'id': 'email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter username', 'id': 'username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter password', 'id': 'password'}),
        }

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email', 'id': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password', 'id': 'password'}))

class TransactionForm(ModelForm):
    class Meta:
        model = transaction
        fields = ['amount', 'description', 'category', 'transaction_type','date']
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter amount'}),
            'description': forms.TextInput(attrs={'placeholder': 'Enter description'}),
            'category': forms.Select(attrs={'placeholder': 'Select category'}),
            'transaction_type': forms.Select(attrs={'placeholder': 'Select transaction type'}),
            'date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select date'}),
        }