# Generated by Django 3.2.10 on 2022-01-18 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_trip_waiting_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('CASH', 'Cash'), ('CARD', 'Card')], default='CASH', max_length=50),
        ),
        migrations.AlterField(
            model_name='trip',
            name='trip_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('SCHEDULED', 'Scheduled'), ('PICKUP', 'Pickup'), ('IN_TRAVEL', 'In Travel'), ('COMPLETE', 'Complete'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=50),
        ),
    ]
