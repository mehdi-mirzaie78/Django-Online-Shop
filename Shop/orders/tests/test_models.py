from django.test import TestCase
from orders.models import Receipt, Order, OrderItem, Coupon
from accounts.models import User
from product.models import Product, Category
from customers.models import Customer
from datetime import datetime, timedelta


class TestReceipt(TestCase):
    def setUp(self):
        self.receipt = Receipt.objects.create(order_details='lenovo|2|1100|2200')

    def test_receipt_creation(self):
        self.assertEqual(self.receipt.order_details, 'lenovo|2|1100|2200')

    def test_receipt_str(self):
        self.assertEqual(self.receipt.__str__(), self.receipt.order_details[:120])


class TestOrder(TestCase):
    def setUp(self):
        user = User.objects.create(
            email='mark@gmail.com',
            phone_number='09182251753',
            full_name='Mark Spector'
        )
        self.customer = Customer.objects.create(user=user, image=None)
        self.order1 = Order.objects.create(
            customer=self.customer,
            discount=10,
        )

        self.order2 = Order.objects.create(customer=self.customer, paid=True)

        self.category = Category.objects.create(name='Laptop', slug='laptop')
        product1 = Product.objects.create(
            name='lenovo',
            slug='lenovo',
            description='One of the best brands',
            price=1000,
            stock=10,
        )
        product1.category.set([self.category])
        product2 = Product.objects.create(
            name='msi',
            slug='msi',
            description='msi is the best',
            price=1000,
            stock=10,
        )
        product2.category.set([self.category])

        self.orderitem1 = OrderItem.objects.create(
            order=self.order1,
            product=product1,
            price=product1.price,
            quantity=2,
        )
        self.orderitem2 = OrderItem.objects.create(
            order=self.order1,
            product=product2,
            price=product2.price,
            quantity=2,
        )
        self.orderitem3 = OrderItem.objects.create(
            order=self.order2,
            product=product1,
            price=product1.price,
            quantity=2,
        )
        self.orderitem4 = OrderItem.objects.create(
            order=self.order2,
            product=product2,
            price=product2.price,
            quantity=2,
        )

    def test_order_creation(self):
        self.assertEqual(self.order1.customer, self.customer)
        self.assertEqual(self.order1.paid, False)
        self.assertEqual(self.order1.discount, 10)

    def test_order_str(self):
        self.assertEqual(self.order1.__str__(), f'{self.customer} - {self.order1.id}')

    def test_order_get_total_price(self):
        self.assertEqual(self.order1.get_total_price(), 3600)
        self.assertEqual(self.order2.get_total_price(), 4000)

    def test_order_get_details(self):
        items = self.order1.items.all()
        res = ''
        for item in items:
            res += item.get_item_details() + '\n'
        self.assertEqual(self.order1.get_details(), res)

    def test_order_create_receipt(self):
        self.assertFalse(self.order1.create_receipt())
        self.assertTrue(bool(self.order2.create_receipt()))


class TestOrderItem(TestCase):

    def setUp(self):
        user = User.objects.create(
            email='mark@gmail.com',
            phone_number='09182251753',
            full_name='Mark Spector'
        )
        self.customer = Customer.objects.create(user=user, image=None)
        self.order = Order.objects.create(customer=self.customer, paid=True)
        self.category = Category.objects.create(name='Laptop', slug='laptop')
        self.product = Product.objects.create(
            name='lenovo',
            slug='lenovo',
            description='One of the best brands',
            price=1000,
            stock=10,
        )

        self.orderitem = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=self.product.price,
            quantity=2,
        )

    def test_order_item_creation(self):
        self.assertEqual(self.orderitem.order, self.order)
        self.assertEqual(self.orderitem.product, self.product)
        self.assertEqual(self.orderitem.price, self.product.price)
        self.assertEqual(self.orderitem.quantity, 2)

    def test_order_item_str(self):
        self.assertEqual(self.orderitem.__str__(), str(self.orderitem.id))

    def test_order_item_get_cost(self):
        self.assertEqual(self.orderitem.get_cost(), 2000)

    def test_order_item_get_item_details(self):
        self.assertEqual(self.orderitem.get_item_details(), 'lenovo|2|1000|2000')

class TestCoupon(TestCase):
    def setUp(self):
        user = User.objects.create(
            email='mark@gmail.com',
            phone_number='09182251753',
            full_name='Mark Spector'
        )
        customer = Customer.objects.create(user=user, image=None)
        self.order = Order.objects.create(customer=customer, paid=True)

        self.coupon = Coupon.objects.create(
            order=self.order,
            code='1234',
            valid_since=datetime.now(),
            valid_until=datetime.now() + timedelta(days=1),
            discount=35,
            active=True
        )

    def test_coupon_creation(self):
        self.assertEqual(self.coupon.order, self.order)
        self.assertEqual(self.coupon.code, '1234')
        self.assertEqual(self.coupon.discount, 35)
        self.assertTrue(self.coupon.active)
        self.assertLess(self.coupon.valid_since, self.coupon.valid_until)


    def test_coupon_str(self):
        self.assertEqual(self.coupon.__str__(), '1234')
