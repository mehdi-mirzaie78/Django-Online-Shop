from django.test import TestCase
from ..models import Customer, Address
from accounts.models import User


class TestCustomerModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='john@gmail.com',
            phone_number='09123456791',
            full_name='John Snow',
            password='abc'
        )
        self.user.groups.create(name='role')
        self.customer = Customer.objects.get(user=self.user)

    def test_customer_str(self):
        self.assertEqual(str(self.customer), 'John Snow')

    def test_customer_save(self):
        self.customer.image = None
        self.customer.save()
        self.assertEqual(self.customer.image, 'default/male.png')

        self.customer.image = 'default/male.png'
        self.customer.save()
        self.assertEqual(self.customer.image, 'default/male.png')

    def test_customer_image_tag(self):
        self.assertEqual(self.customer.image_tag(), '<img src="/media/default/male.png" width="150" height="150" />')
        self.assertTrue(bool(self.customer.image_tag()))

    def test_customer_user_full_name(self):
        self.assertEqual(self.customer.user_full_name(), self.user.full_name)

    def test_customer_phone_number(self):
        self.assertEqual(self.customer.phone_number(), self.user.phone_number)


class TestAddressModel(TestCase):
    def setUp(self):
        customer_test_object = TestCustomerModel()
        customer_test_object.setUp()
        self.customer = customer_test_object.customer

        self.address1 = Address.objects.create(
            customer=self.customer,
            city='Tehran',
            body='Some address',
            postal_code='1234567890'
        )
        self.address2 = Address.objects.create(
            customer=self.customer,
            city='Kermanshah',
            body='Some address',
            postal_code='0987654321'
        )

    def test_address_creation(self):
        self.assertEqual(self.address1.customer, self.customer)
        self.assertEqual(self.address1.city, 'Tehran')
        self.assertEqual(self.address1.body, 'Some address')
        self.assertEqual(self.address1.postal_code, '1234567890')

    def test_address_str(self):
        self.assertEqual(str(self.address1), 'Tehran - Some address')
        self.assertEqual(str(self.address2), 'Kermanshah - Some address')
