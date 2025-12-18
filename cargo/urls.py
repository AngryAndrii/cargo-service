from django.urls import path

from cargo.views import index, TruckListView

urlpatterns = [
    path("", index, name="index"),
    path("trucks/", TruckListView.as_view(), name="truck-list"),
]

app_name = "cargo"
