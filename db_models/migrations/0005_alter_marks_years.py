# Generated by Django 5.0.6 on 2024-12-04 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_models', '0004_categoryfaq'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marks',
            name='years',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]