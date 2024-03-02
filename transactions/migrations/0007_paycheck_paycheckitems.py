# Generated by Django 5.0.2 on 2024-02-26 02:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fin", "0039_alter_account_options"),
        ("transactions", "0006_delete_csv"),
    ]

    operations = [
        migrations.CreateModel(
            name="Paycheck",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("desc", models.CharField(blank=True, max_length=255, null=True)),
                ("added", models.DateTimeField(auto_now_add=True)),
                ("active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="PaycheckItems",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=18,
                        null=True,
                        verbose_name="Amount",
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                ("note", models.CharField(blank=True, max_length=255, null=True)),
                ("added", models.DateTimeField(auto_now_add=True)),
                (
                    "groupedcat",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="fin.groupedcat",
                    ),
                ),
            ],
        ),
    ]
