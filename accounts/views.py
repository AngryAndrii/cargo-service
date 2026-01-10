from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

class DriverLIstView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    template_name = "accounts/driver_list.html"
    # context_object_name = "manufacturers"

    # def get_queryset(self):
    #     return Manufacturer.objects.prefetch_related(
    #         "trucks"
    #     )