# Generated by Django 3.2.10 on 2022-01-05 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(default=50.0)),
                ('payment_time', models.DateTimeField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('origin', models.CharField(max_length=200)),
                ('destination', models.CharField(max_length=200)),
                ('request_time', models.DateTimeField(editable=False)),
                ('price', models.FloatField(default=0.0)),
                ('trip_status', models.CharField(choices=[('PENDING', 'Pending'), ('SCHEDULED', 'Scheduled'), ('PICKUP', 'Pickup'), ('IN_TRAVEL', 'In Travel'), ('COMPLETE', 'Complete')], default='PENDING', max_length=50)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='trips_as_client', to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='trips_as_driver', to=settings.AUTH_USER_MODEL)),
                ('payment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trips.payment')),
            ],
        ),
    ]
