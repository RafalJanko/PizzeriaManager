# Generated by Django 2.2.6 on 2022-03-17 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("PizzeriaManager", "0004_orderitem_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="address",
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
    ]
