# Generated by Django 4.1 on 2023-04-14 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appReservation', '0002_listing_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_number',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
