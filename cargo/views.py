from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
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
        fields = ["service_option", "name", "description", ]

    def __init__(self, *args, **kwargs):
        self.truck = kwargs.pop("truck")
        self.driver = kwargs.pop(
            "driver")
        super().__init__(*args,
                         **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        option = cleaned_data.get("service_option")
        if not option:
            return cleaned_data

        cost = Service.SERVICE_COSTS[option]
        percent = Service.SERVICE_PERCENTS[option]

        driver = getattr(self.truck, "driver", None)
        if not driver:
            raise forms.ValidationError("У цього авто немає драйвера")

        if driver.money < cost:
            raise forms.ValidationError("Недостатньо коштів на рахунку.")

        # стан авто
        if self.truck.condition >= 100:
            raise forms.ValidationError("Авто вже в ідеальному стані.")
        if self.truck.condition + percent > 100:
            cleaned_data["adjust_percent"] = 100 - self.truck.condition
        else:
            cleaned_data["adjust_percent"] = percent

        return cleaned_data


class ServiceCreateView(LoginRequiredMixin, generic.CreateView):
    model = Service
    form_class = ServiceForm
    success_url = reverse_lazy("cargo:service-list")
    template_name = "cargo/service_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["truck"] = self.request.user.truck
        kwargs["driver"] = self.request.user
        return kwargs

    def form_valid(self, form):
        service = form.save(commit=False)
        service.truck = self.request.user.truck

        service._adjust_percent = form.cleaned_data.get(
            "adjust_percent", service.repair_percent
        )

        self.request.user.money -= service.cost
        self.request.user.save()

        service.truck.condition = min(
            100, service.truck.condition + service._adjust_percent
        )
        service.truck.save()

        service.save()

        return super().form_valid(form)
