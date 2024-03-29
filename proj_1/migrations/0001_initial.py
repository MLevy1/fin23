# Generated by Django 5.0.2 on 2024-03-19 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="fcflow",
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
                ("desc", models.CharField(max_length=50)),
                ("ann_freq", models.IntegerField()),
                ("amount", models.DecimalField(decimal_places=2, max_digits=18)),
            ],
        ),
    ]
