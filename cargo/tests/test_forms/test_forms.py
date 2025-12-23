from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cargo.models import Truck, Manufacturer

CREATE_SERVICE_URL=reverse("cargo:service-create")


class FormTest(TestCase):

    def test_login_required(self):
        url = CREATE_SERVICE_URL
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


    def test_truck_queryset_limited_to_user(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        user = get_user_model().objects.create(
            email="test@test.com", password="12345"
        )

        truck = Truck.objects.create(plate_number="JDF1234",
                                     model="test",
                                     manufacturer=manufacturer,
                                     tonnage=5000,
                                     cost_for_rent=1200,
                                     condition=12,
                                     image="testimage")

        other_truck = Truck.objects.create(plate_number="FER1234",
                                     model="test1",
                                     manufacturer=manufacturer,
                                     tonnage=24000,
                                     cost_for_rent=3500,
                                     condition=25,
                                     image="testimage")

        user.truck = truck
        user.save()

        self.client.force_login(user)

        response = self.client.get(reverse("cargo:service-create"))

        form = response.context["form"]
        self.assertEqual(
            list(form.fields["truck"].queryset),
            list(Truck.objects.filter(id=truck.id))
        )
