from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _


class Driver(AbstractUser):
    license_number = models.CharField(max_length=8, unique=True, null=True, blank=True)
    money = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                default=1000)
    truck = models.OneToOneField("Truck",
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 default=None,
                                 related_name="driver"
                                 )

    class Meta:
        ordering = ["username"]


class Truck(models.Model):
    plate_number = models.CharField(max_length=8, unique=True)
    model = models.CharField(max_length=255)
    tonnage = models.PositiveIntegerField()
    manufacturer = models.ForeignKey("Manufacturer",
                                     null=True,
                                     on_delete=models.SET_NULL,
                                     related_name="trucks")
    cost_for_rent = models.DecimalField(max_digits=7,
                                        decimal_places=2,
                                        blank=False,
                                        null=False)
    condition = models.PositiveIntegerField(blank=False, null=False)
    image = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ["condition"]

    def __str__(self):
        return f"{self.manufacturer} {self.model} ({self.plate_number})"



class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=65)
    image = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


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
    planned_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
    driver = models.ForeignKey(Driver,
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL,
                               related_name="orders")

    class Meta:
        ordering = ["id"]


class Service(models.Model):
    SERVICE_CHOICES = [
        ("1", "Option 1 (+1%) — 50"),
        ("2", "Option 2 (+2%) — 100"),
        ("3", "Option 3 (+4%) — 200"),
        ("4", "Option 4 (+8%) — 400"),
        ("5", "Option 5 (+10%) — 500"),
    ]

    SERVICE_COSTS = {
        "1": 50,
        "2": 100,
        "3": 200,
        "4": 400,
        "5": 500,
    }

    SERVICE_PERCENTS = {
        "1": 1,
        "2": 2,
        "3": 4,
        "4": 8,
        "5": 10,
    }

    service_option = models.CharField(max_length=1, choices=SERVICE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=63, )
    description = models.TextField(max_length=255)
    truck = models.ForeignKey(
        "Truck",
        on_delete=models.CASCADE,
        related_name="services"
    )

    @property
    def cost(self) -> int:
        return self.SERVICE_COSTS[self.service_option]

    @property
    def repair_percent(self) -> int:
        return self.SERVICE_PERCENTS[self.service_option]

    def apply(self):
        driver = getattr(self.truck, "driver", None)
        if not driver:
            raise ValidationError("Авто не орендовано, драйвер відсутній.")

        if driver.money < self.cost:
            raise ValidationError("Недостатньо коштів на рахунку.")

        if self.truck.condition >= 100:
            raise ValidationError("Авто вже в ідеальному стані.")

        repair = min(
            self.repair_percent,
            100 - self.truck.condition
        )

        with transaction.atomic():
            driver.money -= self.cost
            driver.save(update_fields=["money"])

            self.truck.condition += repair
            self.truck.save(update_fields=["condition"])

            self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
