# Generated by Django 2.2.6 on 2022-04-19 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PizzeriaManager', '0010_daysoff'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='password',
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=64),
        ),
    ]