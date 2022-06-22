# Generated by Django 2.2.6 on 2022-03-24 20:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("PizzeriaManager", "0006_profile"),
    ]

    operations = [
        migrations.CreateModel(
            name="Shift",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(null=True)),
                (
                    "shift",
                    models.CharField(
                        choices=[
                            ("Morning", "6:00-14:00"),
                            ("Afternoon", "12:00 - 20:00"),
                            ("Evening", "18:00 - 2:00"),
                            ("Night", "0:00 - 8:00"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
