# Generated by Django 2.2.6 on 2022-03-24 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("PizzeriaManager", "0007_shift"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shift",
            name="shift",
            field=models.CharField(
                choices=[
                    ("6:00-14:00", "6:00-14:00"),
                    ("12:00 - 20:00", "12:00 - 20:00"),
                    ("18:00 - 2:00", "18:00 - 2:00"),
                    ("0:00 - 8:00", "0:00 - 8:00"),
                ],
                max_length=50,
            ),
        ),
    ]
