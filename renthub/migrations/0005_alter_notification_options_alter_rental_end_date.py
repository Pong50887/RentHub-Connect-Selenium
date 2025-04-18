# Generated by Django 5.1.2 on 2024-11-06 08:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("renthub", "0004_alter_rental_end_date"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="notification",
            options={"ordering": ["-post_date"]},
        ),
        migrations.AlterField(
            model_name="rental",
            name="end_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 12, 6, 8, 26, 52, 220209, tzinfo=datetime.timezone.utc
                ),
                verbose_name="date checkout",
            ),
        ),
    ]
