from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Driver(AbstractUser):
    license_number = models.CharField(max_length=8)
    money = models.DecimalField(max_digits=10,
                                decimal_places=2)
    truck = models.OneToOneField("Truck",
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 default=None,
                                 related_name="driver"
                                 )


class Truck(models.Model):
    plate_number = models.CharField(max_length=8, unique=True)
    model = models.CharField(max_length=255)
    tonnage = models.PositiveIntegerField()
    manufacturer = models.ForeignKey("Manufacturer",
                                     on_delete=models.SET_NULL,
                                     related_name="trucks")
    cost_for_rent = models.DecimalField(max_digits=7,
                                        decimal_places=2,
                                        blank=False,
                                        null=False)
    condition = models.PositiveIntegerField(blank=False, null=False)
    image = models.ImageField(blank=True, null=True)


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=65)
    image = models.ImageField(blank=True, null=True)


class Order(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "AV", _("Available")
        IN_PROGRESS = "IP", _("In progress")
        COMPLETED = "CO", _("Completed")
    name = models.CharField(max_length=65)
    weight = models.PositiveIntegerField()
    description = models.CharField(max_length=255)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.AVAILABLE,
    )
    payment = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    planned_at = models.DateTimeField(),
    finished_at = models.DateTimeField()
    driver = models.ForeignKey(Driver,
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL,
                               related_name="orders")


class Service(models.Model):
    name = models.CharField(max_length=65)
    description = models.TextField()
    date = models.DateTimeField()
    cost = models.DecimalField(max_digits=7, decimal_places=2)
    truck = models.ForeignKey(Truck,
                              on_delete=models.CASCADE,
                              related_name="services")
