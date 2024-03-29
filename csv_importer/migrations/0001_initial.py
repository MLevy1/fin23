# Generated by Django 5.0.2 on 2024-02-21 04:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("fin", "0038_payee_def_gcat"),
    ]

    operations = [
        migrations.CreateModel(
            name="Csv",
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
                ("file_name", models.FileField(upload_to="csvs")),
                ("uploaded", models.DateTimeField(auto_now_add=True)),
                ("activated", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Imported_Payee",
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
                ("imported_payee", models.CharField(max_length=255, unique=True)),
                ("added", models.DateTimeField(auto_now_add=True)),
                (
                    "payee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="fin.payee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Staged_Transaction",
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
                ("uploaded", models.DateTimeField(auto_now_add=True)),
                ("tdate", models.DateField(blank=True, null=True, verbose_name="Date")),
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
                (
                    "imported_payee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="csv_importer.imported_payee",
                    ),
                ),
            ],
        ),
    ]
