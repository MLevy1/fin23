# Generated by Django 5.0.2 on 2024-03-11 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tax", "0007_alter_inputvalue_multiplier"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="inputvalue",
            name="multiplier",
        ),
        migrations.AddField(
            model_name="tax_return_form_line_input",
            name="multiplier",
            field=models.DecimalField(
                blank=True, decimal_places=4, default=1.0, max_digits=18, null=True
            ),
        ),
    ]
