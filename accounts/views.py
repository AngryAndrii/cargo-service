from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


class DriverLIstView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    template_name = "accounts/driver_list.html"

    def get_queryset(self):
        return get_user_model().objects.select_related(
            "truck", "truck__manufacturer"
        )


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    template_name = "accounts/driver_detail.html"

    def get_queryset(self):
        return get_user_model().objects.select_related(
            "truck", "truck__manufacturer"
        )

from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import DriverCreationForm


class RegisterView(CreateView):
    form_class = DriverCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")