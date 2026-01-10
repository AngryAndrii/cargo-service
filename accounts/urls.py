from django.urls import path

from accounts.views import DriverLIstView

app_name = "accounts"

urlpatterns = [
    path("drivers/", DriverLIstView.as_view(), name="driver-list"),
    # path(
    #     "manufacturers/<int:pk>/manufacturer-detail/",
    #     ManufacturerDetailView.as_view(),
    #     name="manufacturer-detail",
    # ),
]
