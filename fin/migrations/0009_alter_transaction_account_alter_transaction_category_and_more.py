# Generated by Django 4.2.3 on 2023-08-09 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fin', '0008_account_active_payee_active_alter_issue_closedate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='account',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='payee',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]