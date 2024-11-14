# Generated by Django 5.1.3 on 2024-11-14 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AccountsManagementApp', '0003_transaction_expense_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='expense_type',
            field=models.CharField(blank=True, choices=[('Office Supplies', 'Office Supplies'), ('Travel', 'Travel'), ('Utilities', 'Utilities'), ('Salary', 'Salary'), ('Miscellaneous', 'Miscellaneous'), ('GST', 'GST'), ('GeM', 'GeM'), ('ESI', 'ESI')], max_length=15, null=True),
        ),
    ]
