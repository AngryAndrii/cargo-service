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
