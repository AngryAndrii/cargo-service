import datetime

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from cargo.models import Truck, Order, Service


class IndexView(generic.TemplateView):
    template_name = "cargo/index.html"


@login_required
def truck_list(request):
    trucks = Truck.objects.select_related("manufacturer").all()
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


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order


class ServicesListView(LoginRequiredMixin, generic.ListView):
    model = Service
    template_name = "cargo/service_list.html"
    context_object_name = "service_list"

    def get_queryset(self):
        truck = self.request.user.truck
        if not truck:
            return Service.objects.none()
        return truck.services.all()


class ServiceCreateView(LoginRequiredMixin, generic.CreateView):
    model = Service
    fields = "__all__"
    success_url = reverse_lazy("cargo:service-list")
    template_name = "cargo/create_service.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["date"].widget = forms.DateTimeInput(
            attrs={"type": "datetime-local"}
        )
        form.fields["truck"].queryset = Truck.objects.filter(
            id=self.request.user.truck_id
        )
        return form
