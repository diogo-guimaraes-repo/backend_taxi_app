# Generated by Django 3.2.10 on 2022-01-07 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='waiting_time',
            field=models.DurationField(null=True),
        ),
    ]
