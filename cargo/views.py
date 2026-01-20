from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
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


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["service_option", "name", "description"]


class ServiceCreateView(LoginRequiredMixin, generic.CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "cargo/service_form.html"
    success_url = reverse_lazy("cargo:service-list")

    def form_valid(self, form):
        service = form.save(commit=False)
        service.truck = self.request.user.truck

        try:
            service.apply()
        except ValidationError as e:
            form.add_error(None, e.message)
            return self.form_invalid(form)

        return super().form_valid(form)
