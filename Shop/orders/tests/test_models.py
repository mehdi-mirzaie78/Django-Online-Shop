from django.test import TestCase
from orders.models import Order, OrderItem, Coupon
from customers.tests.test_models import TestAddressModel
from product.tests.test_models import TestProduct
from datetime import datetime, timedelta
from django.utils import timezone


class TestCoupon(TestCase):
    def setUp(self):
        self.coupon = Coupon.objects.create(
            code='1234',
            valid_since=datetime.now().replace(tzinfo=timezone.utc),
            valid_until=datetime.now().replace(tzinfo=timezone.utc) + timedelta(days=1),
            discount=35,
        )
        self.coupon2 = Coupon.objects.create(
            code='2312',
            valid_since=datetime.now().replace(tzinfo=timezone.utc) - timedelta(days=1),
            valid_until=datetime.now().replace(tzinfo=timezone.utc),
            discount=12,
        )

    def test_coupon_creation(self):
        self.assertEqual(self.coupon.code, '1234')
        self.assertEqual(self.coupon.discount, 35)
        self.assertTrue(self.coupon.is_active)
        self.assertLess(self.coupon.valid_since, self.coupon.valid_until)

    def test_coupon_str(self):
        self.assertEqual(str(self.coupon), '1234')

    def test_coupon_is_copoun_valid(self):
        self.assertTrue(self.coupon.is_coupon_valid())
        self.assertFalse(self.coupon2.is_coupon_valid())


class TestOrders(TestCase):
    def setUp(self):
        test_address_obj = TestAddressModel()
        test_address_obj.setUp()
        self.customer = test_address_obj.customer
        self.address1 = test_address_obj.address1
        self.address2 = test_address_obj.address2

        self.order1 = Order.objects.create(
            customer=self.customer,
            city=self.address1.city,
            body=self.address1.body,
            postal_code=self.address1.postal_code,
        )

        test_coupon_obj = TestCoupon()
        test_coupon_obj.setUp()
        self.coupon = test_coupon_obj.coupon
        self.order1.coupon = self.coupon

        self.order2 = Order.objects.create(
            customer=self.customer,
            city=self.address2.city,
            body=self.address2.body,
            postal_code=self.address2.postal_code,
            is_paid=True)

        test_product_obj = TestProduct()
        test_product_obj.setUp()
        self.product1 = test_product_obj.product
        self.product2 = test_product_obj.product2

        self.orderitem1 = OrderItem.objects.create(
            order=self.order1,
            product=self.product1,
            price=self.product1.price,
            quantity=2,
        )
        self.orderitem2 = OrderItem.objects.create(
            order=self.order1,
            product=self.product2,
            price=self.product2.price,
            quantity=2,
        )
        self.orderitem3 = OrderItem.objects.create(
            order=self.order2,
            product=self.product1,
            price=self.product1.price,
            quantity=2,
        )
        self.orderitem4 = OrderItem.objects.create(
            order=self.order2,
            product=self.product2,
            price=self.product2.price,
            quantity=2,
        )

    def test_orders_creation(self):
        self.assertEqual(self.order1.customer, self.customer)
        self.assertEqual(self.order1.is_paid, False)
        self.assertEqual(self.order1.discount, 0)
        self.assertEqual(self.order1.city, 'Tehran')
        self.assertEqual(self.order1.body, 'Some address')
        self.assertEqual(self.order1.postal_code, '1234567890')

        self.assertEqual(self.order2.customer, self.customer)
        self.assertEqual(self.order2.is_paid, True)
        self.assertEqual(self.order2.discount, 0)
        self.assertEqual(self.order2.city, 'Kermanshah')
        self.assertEqual(self.order2.body, 'Some address')
        self.assertEqual(self.order2.postal_code, '0987654321')

    def test_orders_str(self):
        self.assertEqual(str(self.order1), f'{self.customer} - {self.order1.id}')
        self.assertEqual(str(self.order1), f'{self.customer} - {self.order1.id}')

    def test_orders_apply_coupon(self):
        self.order1.apply_coupon()
        self.assertEqual(self.order1.discount, self.coupon.discount)

    def test_orders_get_total_price(self):
        self.order1.apply_coupon()
        self.assertEqual(self.order1.get_total_price(), 2600)
        self.assertEqual(self.order2.get_total_price(), 4000)

    def test_orders_check_address(self):
        self.assertTrue(self.order1.check_address())
        self.assertTrue(self.order2.check_address())


class TestOrderItem(TestCase):

    def setUp(self):
        test_orders_obj = TestOrders()
        test_orders_obj.setUp()
        self.order = test_orders_obj.order1
        self.product1 = test_orders_obj.product1
        self.product2 = test_orders_obj.product2

        self.orderitem1 = OrderItem.objects.create(
            order=self.order,
            product=self.product1,
            price=self.product1.price,
            quantity=2,
        )
        self.orderitem2 = OrderItem.objects.create(
            order=self.order,
            product=self.product2,
            price=self.product2.price,
            quantity=2,
        )

    def test_order_item_creation(self):
        self.assertEqual(self.orderitem1.order, self.order)
        self.assertEqual(self.orderitem1.product, self.product1)
        self.assertEqual(self.orderitem1.price, self.product1.price)
        self.assertEqual(self.orderitem1.quantity, 2)

        self.assertEqual(self.orderitem2.order, self.order)
        self.assertEqual(self.orderitem2.product, self.product2)
        self.assertEqual(self.orderitem2.price, self.product2.price)
        self.assertEqual(self.orderitem2.quantity, 2)

    def test_order_item_str(self):
        self.assertEqual(str(self.orderitem1), str(self.orderitem1.id))
        self.assertEqual(str(self.orderitem2), str(self.orderitem2.id))

    def test_order_item_get_cost(self):
        self.assertEqual(self.orderitem1.get_cost(), 2000)
        self.assertEqual(self.orderitem2.get_cost(), 2000)

    def test_order_itme_check_status(self):
        self.assertTrue(self.orderitem1.check_status())
        self.assertTrue(self.orderitem2.check_status())
