from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from cargo.models import Truck, Order, Service, Manufacturer


class IndexView(generic.TemplateView):
    template_name = "cargo/index.html"


class TruckListView(LoginRequiredMixin, generic.ListView):
    model = Truck
    paginate_by = 5
    template_name = "cargo/truck_list.html"

    def get_queryset(self):
        return Truck.objects.select_related("manufacturer")

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["cargo/truck_list_item.html"]
        return ["cargo/truck_list.html"]


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturers"

    def get_queryset(self):
        return Manufacturer.objects.prefetch_related(
            "trucks"
        )


class ManufacturerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Manufacturer

    def get_queryset(self):
        return Manufacturer.objects.prefetch_related(
            "trucks"
        )


class TruckDetailView(LoginRequiredMixin, generic.DetailView):
    model = Truck


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order


class ServicesListView(LoginRequiredMixin, generic.ListView):
    model = Service

    def get_queryset(self):
        truck = self.request.user.truck
        if not truck:
            return Service.objects.none()
        return truck.services.all()


class ServiceCreateView(LoginRequiredMixin, generic.CreateView):
    model = Service
    fields = "__all__"
    success_url = reverse_lazy("cargo:service-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["date"].widget = forms.DateTimeInput(
            attrs={"type": "datetime-local"}
        )
        form.fields["truck"].queryset = Truck.objects.filter(
            id=self.request.user.truck_id
        )
        return form
