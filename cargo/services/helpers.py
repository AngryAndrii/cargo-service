from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from cargo.models import Truck, Driver


@login_required
def rent_truck(request, pk):
    if request.method != "POST":
        return redirect("cargo:truck-list")

    driver: Driver = request.user
    truck = get_object_or_404(Truck, pk=pk)

    # 1️⃣ якщо водій вже має трак
    if driver.truck is not None:
        messages.error(request, "You've already rented a truck!")
        return redirect("cargo:truck-list")

    # 2️⃣ якщо трак вже орендований
    if Driver.objects.filter(truck=truck).exists():
        messages.error(request, "This truck rented by another driver!")
        return redirect("cargo:truck-list")

    # 3️⃣ якщо не вистачає грошей
    if driver.money < truck.cost_for_rent:
        messages.error(request, "Not enough money to rent this truck")
        return redirect("cargo:truck-list")

    # 4️⃣ усе разом — атомарно
    with transaction.atomic():
        driver.money -= truck.cost_for_rent
        driver.truck = truck
        driver.save()
    messages.success(request, "Truck successfully rented!")

    return redirect("cargo:truck-list")
