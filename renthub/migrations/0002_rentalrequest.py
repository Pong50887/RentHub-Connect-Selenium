# Generated by Django 5.1 on 2024-10-16 14:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renthub', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentalRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='room_images/')),
                ('renter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='renthub.renter')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='renthub.room')),
            ],
        ),
    ]
