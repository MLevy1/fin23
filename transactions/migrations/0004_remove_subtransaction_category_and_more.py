# Generated by Django 4.2.3 on 2023-12-27 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_alter_subtransaction_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subtransaction',
            name='category',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='category',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='groupedcat',
        ),
    ]
