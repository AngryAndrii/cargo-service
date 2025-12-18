from django.shortcuts import render

import datetime
from django.shortcuts import render
from django.views import generic

from cargo.models import Truck, Order, Service


def index(request):
 context = {
   "time": datetime.datetime.now(),
   }
 return render(request, "cargo/index.html", context=context)


class TruckListView(generic.ListView):
    model = Truck


class OrderListView(generic.ListView):
    model = Order
    context_object_name = "order_list"

class ServicesListView(generic.ListView):
    model = Service
    context_object_name = "service_list"
