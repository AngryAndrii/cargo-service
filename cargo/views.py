import datetime

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import generic

from cargo.models import Truck, Order, Service


def index(request):
    context = {
        "time": datetime.datetime.now(),
    }
    return render(request, "cargo/index.html", context=context)


def truck_list(request):
    trucks = Truck.objects.all()
    paginator = Paginator(trucks, 5)
    page_number = request.GET.get('page', 1)
    try:
        page_number = int(page_number)
    except ValueError:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    if request.headers.get("HX-Request") == "true":
        return render(request, "cargo/truck_list_item.html", {"truck_list": page_obj})

    return render(request, "cargo/truck_list.html", {"truck_list": page_obj})


class OrderListView(generic.ListView):
    model = Order


class OrderDetailView(generic.DetailView):
    model = Order


class ServicesListView(generic.ListView):
    model = Service
