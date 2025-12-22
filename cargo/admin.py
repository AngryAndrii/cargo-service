from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from cargo.models import Truck, Service, Order, Manufacturer

driver = get_user_model()


@admin.register(driver)
class DriverAdmin(UserAdmin):
    model = driver

    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("license_number", "money", "truck")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "license_number",
                )
            },
        ),
    )


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    model = Truck

    list_display = ["manufacturer", "model", "tonnage", "condition"]

admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Manufacturer)
