from django import forms



choices=[('Rent','Rent'),
        ('Grocesries','Groceries'),
        ('Insurance','Insurance'),
        ('Healthcare','Healthcare'),
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Entertainment', 'Entertainment'),
        ('Utilities', 'Utilities'),
        ('Shopping','Shopping'),
        ('Financial','Financial'),
        ('Household','Household'),
        ('Miscellaneous', 'Miscellaneous'),
        ('Other','Other'),
        ('Primary Income','Primary Income'),
        ('Passive Income','Passive Income'),
        ('Other Income','Other Income'),
    ]

class filters(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'id':'start_date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'id':'end_date'}))
    category = forms.ChoiceField(choices=choices, required=False, widget=forms.Select(attrs={'id':'category'}))
    min_amount = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Min Amount', 'id':'min_amount'}))
    max_amount = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Max Amount', 'id':'max_amount'}))
    transaction_type = forms.ChoiceField(choices=[('Income', 'Income'), ('Expense', 'Expense')], required=False,widget=forms.Select(attrs={'id':'transaction_type'}))