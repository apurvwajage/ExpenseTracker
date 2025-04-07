from django.forms import ModelForm
from django import forms
from core.models import transaction

class ExpenseForm(ModelForm):
    class Meta:
        model = transaction
        fields = ['amount', 'description', 'category', 'transaction_type','date']
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter amount', 'id': 'amount'}),
            'description': forms.TextInput(attrs={'placeholder': 'Enter description', 'id': 'description'}),
            'category': forms.Select(attrs={'placeholder': 'Select category', 'id': 'category'}),
            'date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select date', 'id': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        # Set the initial value for transaction_type to 'Expense'
        self.fields['transaction_type'].initial = 'Expense'


class IncomeForm(ModelForm):
    class Meta:
        model = transaction
        fields = ['amount', 'description', 'category', 'transaction_type','date']
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter amount', 'id': 'amount'}),
            'description': forms.TextInput(attrs={'placeholder': 'Enter description', 'id': 'description'}),
            'category': forms.Select(attrs={'placeholder': 'Select category', 'id': 'category'}),
            'date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select date', 'id': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        # Set the initial value for transaction_type to 'Income'
        self.fields['transaction_type'].initial = 'Income'


class PDFform(forms.Form):
    pdf = forms.FileField(
        label='Select PDF file',
        help_text='Max. 42 megabytes',
        widget=forms.ClearableFileInput()
    )