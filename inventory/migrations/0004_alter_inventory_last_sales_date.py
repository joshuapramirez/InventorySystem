# Generated by Django 4.2.4 on 2023-08-13 23:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0003_alter_inventory_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inventory",
            name="last_sales_date",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
