from django.urls import path

from cargo.views import index, TruckListView, OrderListView, ServicesListView

urlpatterns = [
    path("", index, name="index"),
    path("trucks/", TruckListView.as_view(), name="truck-list"),
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("services/", ServicesListView.as_view(), name="service-list")
]

app_name = "cargo"
