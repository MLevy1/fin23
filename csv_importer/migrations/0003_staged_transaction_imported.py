# Generated by Django 4.2.10 on 2024-02-23 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("csv_importer", "0002_staged_transaction_account"),
    ]

    operations = [
        migrations.AddField(
            model_name="staged_transaction",
            name="imported",
            field=models.BooleanField(default=False),
        ),
    ]