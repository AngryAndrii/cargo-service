from django.shortcuts import render

import datetime
from django.shortcuts import render
from django.views import generic

from cargo.models import Truck


def index(request):
 context = {
   "time": datetime.datetime.now(),
   }
 return render(request, "cargo/index.html", context=context)


class TruckListView(generic.ListView):
    model = Truck

