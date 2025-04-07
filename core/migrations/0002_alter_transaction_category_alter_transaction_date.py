# Generated by Django 5.1.7 on 2025-04-02 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.CharField(choices=[('Rent', 'Rent'), ('Grocesries', 'Groceries'), ('Insurance', 'Insurance'), ('Healthcare', 'Healthcare'), ('Food', 'Food'), ('Transport', 'Transport'), ('Entertainment', 'Entertainment'), ('Utilities', 'Utilities'), ('Shopping', 'Shopping'), ('Financial', 'Financial'), ('Household', 'Household'), ('Miscellaneous', 'Miscellaneous'), ('Other', 'Other'), ('Primary Income', 'Primary Income'), ('Passive Income', 'Passive Income'), ('Other Income', 'Other Income')], default='Other', max_length=100),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(),
        ),
    ]
