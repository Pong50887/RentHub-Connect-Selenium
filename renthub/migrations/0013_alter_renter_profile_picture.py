# Generated by Django 5.1.2 on 2024-11-14 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("renthub", "0012_renter_profile_picture_renter_thai_citizenship_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="renter",
            name="profile_picture",
            field=models.ImageField(
                blank=True, default="default.png", upload_to="profile_images/"
            ),
        ),
    ]
