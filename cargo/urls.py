from django.urls import path

from cargo.services.helpers import rent_truck, take_order_modal, take_order, \
    complete_order_modal, complete_order
from cargo.views import index, TruckListView, OrderListView, ServicesListView, \
    OrderDetailView

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
    path("orders/<int:pk>/",
         OrderDetailView.as_view(),
         name="order-detail"),
    path(
        "orders/<int:pk>/take/modal/",
        take_order_modal,
        name="take-order-modal",
    ),
    path(
        "orders/<int:pk>/take/",
        take_order,
        name="take-order",
    ),
    path(
        "orders/<int:pk>/complete/modal/",
        complete_order_modal,
        name="complete-order-modal",
    ),
    path(
        "orders/<int:pk>/complete/",
        complete_order,
        name="complete-order",
    ),
]

app_name = "cargo"
