from email.mime import message
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save
from ..users.models import User
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


class Payment(models.Model):

    class PaymentMethods(models.TextChoices):
        CASH = "CASH", "Cash"
        CARD = "CARD", "Card"
        TWINT = "TWINT", "Twint"
        CREDIT = "CREDIT", "Credit"

    value = models.FloatField(default=0.0, blank=False)
    payment_time = models.DateTimeField(editable=False)
    payment_method = models.CharField(
        max_length=50, choices=PaymentMethods.choices, default=PaymentMethods.CASH)

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
        CANCELLED = "CANCELLED", "Cancelled"

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

    def pay_trip(self, payment_data):
        self.price = payment_data["value"]
        if payment_data["payment_method"] == Payment.PaymentMethods.CREDIT:
            user = User.objects.get(id=self.client.id)
            if user.client.use_credit(self.price) == "INSUFFICIENT_FUNDS":
                return "INSUFFICIENT_FUNDS"

        self.trip_status = Trip.Status.COMPLETE
        self.payment = Payment.objects.create(**payment_data)
        self.save()
        return "SUCCESS"

    def cancel_trip(self):
        self.trip_status = Trip.Status.CANCELLED
        self.save()


def send_trip_confirmation(instance, from_email):
    subject = 'Your Trip Request'
    message = '%s your trip request was submitted. We will assign a driver and let you know the waiting time shortly. Thank you!' % (
        instance.client.first_name)
    return subject, message


def send_trip_scheduled(instance, from_email):
    if instance.driver:
        subject = 'Trip Scheduled'
        subject_driver = 'You have a new trip assigned.'
        message = '%s your trip is scheduled with driver %s. We will let you know the second he is on your way' % (
            instance.client.first_name, instance.driver.first_name)
        message_driver = '%s you have a new trip scheduled for client %s %s. You can reach him at %s.' % (
            instance.driver.first_name, instance.client.first_name, instance.client.last_name, instance.client.phone_number)
        send_mail(subject_driver, message_driver, from_email, [instance.driver.email], fail_silently=False)
        return subject, message


def send_trip_in_pickup(instance, from_email):
    subject = 'Your car is on your way'
    message = '%s your car is on your way to pick you up. Our driver will call you once he has arrived.' % (
        instance.client.first_name)
    return subject, message


def send_trip_complete(instance, from_email):
    subject = 'Thank you for using ECOTAXIRICARDO'
    message = '%d thank you so much for using our services. We cant wait to see you again.' % (
        instance.client.first_name)
    return subject, message


def send_trip_cancelled(instance, from_email):
    subject = 'Cancellation confirmed'
    message = '%s your trip has been cancelled. We are looking forward to hearing from you in the future.' % (
        instance.client.first_name)
    if instance.driver:
        subject_driver = 'Trip cancelled'
        message_driver = '%s, %s %s has cancelled his trip.' % (
            instance.driver.first_name, instance.client.first_name, instance.client.last_name)
        send_mail(subject_driver, message_driver, from_email, [instance.driver.email], fail_silently=False)
    return subject, message


notification_methods = {
    'PENDING': send_trip_confirmation,
    'SCHEDULED': send_trip_scheduled,
    'PICKUP': send_trip_in_pickup,
    'COMPLETE': send_trip_complete,
    'CANCELLED': send_trip_cancelled
}


@receiver(pre_save, sender=Trip)
def send_trip_updates(sender, instance, **kwargs):
    send_update = False
    try:
        obj = sender.objects.get(id=instance.id)
    except sender.DoesNotExist:
        send_update = True
    else:
        if not obj.trip_status == instance.trip_status:
            send_update = True
    if send_update:
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = instance.client.email
        try:
            subject, message = notification_methods[instance.trip_status](instance, from_email)
            message += '\n\n Best regards, ECOTAXIRICARDO'
            send_mail(subject, message, from_email, [to_email], fail_silently=False)
        except:
            pass
