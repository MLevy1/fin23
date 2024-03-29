# Generated by Django 4.2.3 on 2023-11-02 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fin', '0022_jobs_l1group_location'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Jobs',
            new_name='Job',
        ),
        migrations.AddField(
            model_name='category',
            name='l1group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fin.l1group'),
        ),
        migrations.AlterField(
            model_name='l1group',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='l1group',
            name='l1group',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
