# Generated by Django 4.2.3 on 2023-07-28 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fin', '0003_transaction_tid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='tid',
            field=models.IntegerField(null=True),
        ),
    ]
