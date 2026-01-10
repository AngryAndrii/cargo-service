from django.urls import path

from accounts.views import DriverLIstView, DriverDetailView

app_name = "accounts"

urlpatterns = [
    path("drivers/", DriverLIstView.as_view(), name="driver-list"),
    path(
        "drivers/<int:pk>/driver-detail/",
        DriverDetailView.as_view(),
        name="driver-detail",
    ),
]
