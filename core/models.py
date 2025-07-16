from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class users(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
class transaction(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    amount = models.FloatField()
    description = models.CharField(max_length=400)
    date = models.DateField()
    category = models.CharField(max_length=100, choices=[
        ('Rent','Rent'),
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
    ], default = 'Other')
    transaction_type = models.CharField(max_length=10, choices=[
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ])

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.description}"