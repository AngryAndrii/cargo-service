from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST

from cargo.models import Truck, Driver, Order


@login_required
def rent_truck(request, pk):
    if request.method != "POST":
        return redirect("cargo:truck-list")

    driver: Driver = request.user
    truck = get_object_or_404(Truck, pk=pk)

    if driver.truck is not None:
        messages.error(request, "You've already rented a truck!")
        return redirect("cargo:truck-list")

    if Driver.objects.filter(truck=truck).exists():
        messages.error(request, "This truck rented by another driver!")
        return redirect("cargo:truck-list")

    if driver.money < truck.cost_for_rent:
        messages.error(request, "Not enough money to rent this truck")
        return redirect("cargo:truck-list")

    with transaction.atomic():
        driver.money -= truck.cost_for_rent
        driver.truck = truck
        driver.save()
    messages.success(request, "Truck successfully rented!")

    return redirect("cargo:truck-list")


def take_order_modal(request, pk):
    order = get_object_or_404(Order, pk=pk)

    return render(
        request,
        "includes/confirm_modal.html",
        {
            "modal_id": "take-order-modal",
            "title": "Take order",
            "body": f"Are you sure you want to take order '{order.name}'?",
            "confirm_text": "Take order",
            "action_url": reverse("cargo:take-order", args=[pk]),
        },
    )


@require_POST
def take_order(request, pk):
    order = get_object_or_404(Order, pk=pk)

    driver: Driver = request.user

    if order.status == "IP":
        messages.error(request, "This order is already being fulfilled!")
        return redirect("cargo:order-detail", pk=pk)

    if order.status == "CO":
        messages.error(request, "this order has already been fulfilled!")
        return redirect("cargo:order-detail", pk=pk)

    if driver.truck.tonnage < order.weight:
        messages.error(request, "Your car does not have enough load capacity.")
        return redirect("cargo:order-detail", pk=pk)

    order.status = Order.Status.IN_PROGRESS
    order.driver = driver
    order.save()
    messages.success(request, "You've just taken this order!")

    return HttpResponse(
        '<script>window.location.reload()</script>'
    )


def complete_order_modal(request, pk):
    order = get_object_or_404(Order, pk=pk)

    return render(
        request,
        "includes/confirm_modal.html",
        {
            "modal_id": "complete-order-modal",
            "title": "Complete",
            "body": f"Are you sure you want complete order '{order.name}'?",
            "confirm_text": "Complete order",
            "action_url": reverse("cargo:complete-order", args=[pk]),
        },
    )


@require_POST
def complete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)

    driver: Driver = request.user

    with transaction.atomic():
        driver.money += order.payment
        order.status = Order.Status.COMPLETED
        order.save()
        driver.save()
    messages.success(request, "Order successfully completed! money transferred to your account")

    return HttpResponse(
        '<script>window.location.reload()</script>'
    )
