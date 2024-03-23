# Generated by Django 5.0.2 on 2024-03-19 07:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tax", "0009_remove_tax_return_form_line_input_amount_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tax_Return_Form_Subtotal",
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
                ("subtotal", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "multiplier",
                    models.DecimalField(
                        blank=True,
                        decimal_places=4,
                        default=1.0,
                        max_digits=18,
                        null=True,
                    ),
                ),
                (
                    "inputvalue",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="tax.inputvalue",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="tax_return_form_line_input",
            name="subtotal",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="tax.tax_return_form_subtotal",
            ),
        ),
    ]
