from django.contrib.auth import get_user_model
from django.test import TestCase

from cargo.models import Truck, Manufacturer


class ModelTest(TestCase):
    def test_truck_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        truck = Truck.objects.create(plate_number="JDF1234",
                                     model="test",
                                     manufacturer=manufacturer,
                                     tonnage=5000,
                                     cost_for_rent=1200,
                                     condition=12,
                                     image="testimage")
        self.assertEqual(str(truck),
                         f"{truck.manufacturer} {truck.model} ({truck.plate_number})")

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        self.assertEqual(str(manufacturer), manufacturer.name)

    def test_create_user_with_added_fields(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        truck = Truck.objects.create(plate_number="JDF1234",
                                     model="test",
                                     manufacturer=manufacturer,
                                     tonnage=5000,
                                     cost_for_rent=1200,
                                     condition=12,
                                     image="testimage")
        license_number = "123qwe"
        money = 2300
        driver = get_user_model().objects.create(
            username="test",
            password="123test123",
            license_number="123qwe",
            money=2300,
            truck=truck
        )

        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.money, money)
        self.assertEqual(driver.truck, truck)
