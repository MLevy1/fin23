# Generated by Django 4.2.3 on 2023-11-28 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fin', '0029_alter_payee_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budgetitem',
            name='itemCat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='fin.category'),
        ),
        migrations.AlterField(
            model_name='groupedcat',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='fin.category'),
        ),
        migrations.AlterField(
            model_name='groupedcat',
            name='l1group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='fin.l1group'),
        ),
        migrations.AlterField(
            model_name='l1group',
            name='aligned_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='fin.category'),
        ),
        migrations.AlterField(
            model_name='trans',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fin.account'),
        ),
        migrations.AlterField(
            model_name='trans',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fin.category'),
        ),
        migrations.AlterField(
            model_name='trans',
            name='groupedcat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='fin.groupedcat'),
        ),
        migrations.AlterField(
            model_name='trans',
            name='payee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fin.payee'),
        ),
    ]