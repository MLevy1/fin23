# Generated by Django 4.2.3 on 2023-07-27 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_member_joined_date_member_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='phone',
        ),
        migrations.AlterField(
            model_name='member',
            name='joined_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]