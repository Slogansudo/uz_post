# Generated by Django 5.0.6 on 2024-12-08 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postaloffice',
            name='index',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='postaloffice',
            name='working_days',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='postaloffice',
            name='working_hours',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]