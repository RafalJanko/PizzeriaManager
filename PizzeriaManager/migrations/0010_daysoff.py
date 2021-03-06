# Generated by Django 2.2.6 on 2022-03-25 19:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("PizzeriaManager", "0009_auto_20220325_0034"),
    ]

    operations = [
        migrations.CreateModel(
            name="DaysOff",
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
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "reason",
                    models.CharField(
                        choices=[
                            ("Paid time off", "Paid time off"),
                            ("Unpaid leave", "Unpaid leave"),
                            ("On demand", "On demand"),
                            ("Bereavement", "Bereavement"),
                        ],
                        max_length=30,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Accepted", "Accepted"),
                            ("Denied", "Denied"),
                        ],
                        default="Pending",
                        max_length=30,
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
