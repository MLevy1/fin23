# Generated by Django 4.2.3 on 2023-10-16 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fin', '0013_historicaltrans_historicalpayee_historicalaccount'),
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemName', models.CharField(max_length=100, verbose_name='Issue Name')),
                ('itemFreq', models.CharField(choices=[(1, 'Annual'), (4, 'Quarterly'), (12, 'Monthly')], default=12, max_length=20, verbose_name='Frequency')),
            ],
        ),
    ]
