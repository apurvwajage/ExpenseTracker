# Generated by Django 5.1.7 on 2025-04-06 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_transaction_category_alter_transaction_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='url',
            new_name='fileName',
        ),
    ]
