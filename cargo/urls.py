from django.urls import path

from cargo.services.helpers import rent_truck
from cargo.views import index, TruckListView, OrderListView, ServicesListView

urlpatterns = [
    path("", index, name="index"),
    path("trucks/", TruckListView.as_view(), name="truck-list"),
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("services/", ServicesListView.as_view(), name="service-list"),
    path(
        "cars/<int:pk>/rent-truck/",
        rent_truck,
        name="rent-truck",
    ),

]

app_name = "cargo"
