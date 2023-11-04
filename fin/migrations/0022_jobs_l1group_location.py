# Generated by Django 4.2.3 on 2023-11-02 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fin', '0021_alter_budgetitem_itemfreq'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employer', models.CharField(blank=True, max_length=255, null=True)),
                ('job_title', models.CharField(blank=True, max_length=255, null=True)),
                ('salary', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True, verbose_name='Amount')),
                ('bonus', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True, verbose_name='Amount')),
                ('state', models.CharField(blank=True, max_length=2, null=True)),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Date')),
            ],
        ),
        migrations.CreateModel(
            name='L1Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('l1group', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True, verbose_name='Active')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Date')),
            ],
        ),
    ]
