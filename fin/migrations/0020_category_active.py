# Generated by Django 4.2.3 on 2023-10-20 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fin', '0019_historicaltrans_tag_trans_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
    ]