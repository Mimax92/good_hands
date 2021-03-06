# Generated by Django 3.1.3 on 2020-11-09 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20201108_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='zip_code',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='instytution',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(3, 'domyślnie fundacja'), (0, 'fundacja'), (2, 'zbiórka lokalna'), (1, 'organizacja pozarządowa')]),
        ),
    ]
