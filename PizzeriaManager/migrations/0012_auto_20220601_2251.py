# Generated by Django 3.1.12 on 2022-06-01 20:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('PizzeriaManager', '0011_auto_20220601_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]