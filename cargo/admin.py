from django.contrib import admin
from django.contrib.auth import get_user_model

from cargo.models import Truck, Service, Order, Manufacturer

admin.site.register(get_user_model())
admin.site.register(Truck)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Manufacturer)
