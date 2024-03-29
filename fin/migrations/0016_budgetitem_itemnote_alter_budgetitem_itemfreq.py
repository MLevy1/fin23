# Generated by Django 4.2.3 on 2023-10-17 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fin', '0015_budgetitem_itemamt_alter_budgetitem_itemfreq'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetitem',
            name='itemNote',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Note'),
        ),
        migrations.AlterField(
            model_name='budgetitem',
            name='itemFreq',
            field=models.CharField(choices=[('Annual', 'Annual'), ('Semiannual', 'Semi-Annual'), ('Quarterly', 'Quarterly'), ('Monthly', 'Monthly'), ('Biweekly', 'Bi-Weekly'), ('Weekly', 'Weekly'), ('Daily', 'Daily'), ('Officedays', 'Office Days'), ('Homeworkdays', 'Work-from-home Days'), ('Weekenddays', 'Weekend Days'), ('Vactiondays', 'Vacation Days'), ('Varible', 'Variable')], default='Monthly', max_length=20, verbose_name='Frequency'),
        ),
    ]
