# Generated by Django 5.0.2 on 2024-03-06 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0010_remove_paycheckitems_active_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="paycheckitems",
            name="paycheck",
        ),
        migrations.RemoveField(
            model_name="paycheckitems",
            name="groupedcat",
        ),
        migrations.DeleteModel(
            name="Paycheck",
        ),
        migrations.DeleteModel(
            name="PaycheckItems",
        ),
    ]
