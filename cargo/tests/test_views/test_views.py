from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cargo.models import Truck, Manufacturer, Order

TRUCK_LIST_URL = reverse("cargo:truck-list")
ORDER_LIST_URL = reverse("cargo:order-list")


class PublicTruckListTest(TestCase):

    def test_login_required(self):
        res = self.client.get(TRUCK_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTruckListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="test",
                                                         password="test12345",
                                                         )
        self.client.force_login(self.user)

    def test_retrieve_truck_list(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        Truck.objects.create(plate_number="JDF1234",
                             model="test",
                             manufacturer=manufacturer,
                             tonnage=5000,
                             cost_for_rent=1200,
                             condition=12,
                             image="testimage")
        res = self.client.get(TRUCK_LIST_URL)
        self.assertEqual(res.status_code, 200)
        trucks = Truck.objects.all()
        self.assertEqual(list(res.context["truck_list"]), list(trucks))


class PublicOrderListTest(TestCase):

    def test_login_required(self):
        res = self.client.get(ORDER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateOrderListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="test",
                                                         password="test12345",
                                                         )
        self.client.force_login(self.user)

    def test_retrieve_order_list(self):
        Order.objects.create(name="test",
                             weight=3400,
                             description="test description",
                             status="AV",
                             payment=234,
                             created_at=datetime(2025, 12, 16, 10, 0),
                             planned_at=datetime(2025, 12, 16, 10, 0),
                             finished_at=datetime(2025, 12, 16, 10, 0),
                             driver=self.user)
        res = self.client.get(ORDER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        orders = Order.objects.all()
        self.assertEqual(list(res.context["order_list"]), list(orders))
