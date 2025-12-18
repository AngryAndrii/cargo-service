from django.urls import path

from cargo.views import index, TruckListView, OrderListView

urlpatterns = [
    path("", index, name="index"),
    path("trucks/", TruckListView.as_view(), name="truck-list"),
    path("orders/", OrderListView.as_view(), name="order-list"),
]

app_name = "cargo"
