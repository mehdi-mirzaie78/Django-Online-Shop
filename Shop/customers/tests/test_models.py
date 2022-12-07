from django.test import TestCase
from ..models import Customer, Address
from accounts.models import User


class TestCustomerModel(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            email='john@email.com',
            phone_number='09123456789',
            full_name='John Doe'
        )
        self.user2 = User.objects.create(
            email='jack@email.com',
            phone_number='09123456792')

        self.customer = Customer.objects.create(user=self.user1)

    def test_customer_str(self):
        self.assertEqual(str(self.customer), 'John Doe')

    def test_customer_str_with_no_full_name(self):
        customer = Customer.objects.create(user=self.user2)


class TestAddressModel(TestCase):
    def setUp(self):
        customer_test_object = TestCustomerModel()
        customer_test_object.setUp()
        self.customer = customer_test_object.customer

    def test_address_str(self):
        address = Address.objects.create(
            customer=self.customer,
            city='Tehran',
            body='Some address',
            postal_code='1234567890'
        )
        self.assertEqual(str(address), 'Tehran - Some address')
