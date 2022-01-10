from django.db import models
from django.utils import timezone
from ..users.models import User
import uuid
from django.urls import reverse


class Payment(models.Model):
    value = models.FloatField(default=50.0, blank=False)
    payment_time = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.payment_time = timezone.now()
        return super().save(*args, **kwargs)


class Trip(models.Model):

    class Status(models.TextChoices):
        PENDING_CONFIRMATION = "PENDING", "Pending"
        SCHEDULED = "SCHEDULED", "Scheduled"
        PICKUP = "PICKUP", "Pickup"
        IN_TRAVEL = "IN_TRAVEL", "In Travel"
        COMPLETE = "COMPLETE", "Complete"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, related_name="trips_as_client")
    driver = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name="trips_as_driver")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    origin = models.CharField(max_length=200, blank=False)
    destination = models.CharField(max_length=200, blank=False)
    request_time = models.DateTimeField(editable=False)
    waiting_time = models.DurationField(null=True)
    price = models.FloatField(default=0.0)
    trip_status = models.CharField(
        max_length=50, choices=Status.choices, default=Status.PENDING_CONFIRMATION)

    def __str__(self):
        """
        string representation
        :return:
        """
        return f'{self.id}'

    def get_absolute_url(self):
        return reverse('trip:trip_detail', kwargs={'trip_id': self.id})
