from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST

from cargo.models import Truck, Driver, Order


def rent_truck_modal(request, pk):
    truck = get_object_or_404(Truck, pk=pk)

    return render(
        request,
        "includes/confirm_modal.html",
        {
            "modal_id": "rent-truck-modal",
            "title": "Rent truck",
            "body": f"Are you sure you want to rent truck {truck.manufacturer}"
                    f" {truck.model} with '{truck.plate_number}' number?",
            "confirm_text": "Rent truck",
            "action_url": reverse("cargo:rent-truck", args=[pk]),
        },
    )


@login_required
def rent_truck(request, pk):
    if request.method != "POST":
        return redirect("cargo:truck-list")

    driver: Driver = request.user
    truck = get_object_or_404(Truck, pk=pk)

    if driver.truck is not None:
        messages.error(request, "You already have a truck!")
        return HttpResponse('<script>window.location.reload()</script>')

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

    return HttpResponse('<script>window.location.reload()</script>')


def return_truck_modal(request, pk):
    truck = get_object_or_404(Truck, pk=pk)

    return render(
        request,
        "includes/confirm_modal.html",
        {
            "modal_id": "return-truck-modal",
            "title": "Return truck",
            "body": f"Are you sure you want to return truck '{truck.plate_number}'?",
            "confirm_text": "Return truck",
            "action_url": reverse("cargo:return-truck", args=[pk]),
        },
    )


@require_POST
def return_truck(request, pk):
    truck = get_object_or_404(Truck, pk=pk)
    driver: Driver = request.user

    if driver.truck != truck:
        messages.error(request, "This truck is not assigned to you.")
        return redirect("cargo:truck-list")

    has_active_orders = driver.orders.filter(
        status=Order.Status.IN_PROGRESS
    ).exists()

    if has_active_orders:
        messages.error(
            request,
            "You cannot return the truck while you have active orders."
        )
        return redirect("cargo:truck-detail", pk=pk)

    driver.truck = None
    driver.save()

    messages.success(request, "Truck has been successfully returned.")
    return HttpResponse('<script>window.location.reload()</script>')


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

    if order.status != Order.Status.AVAILABLE:
        messages.error(request, "Order is not available.")
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
    messages.success(request,
                     "Order successfully completed! money transferred to your account")

    return HttpResponse(
        '<script>window.location.reload()</script>'
    )
