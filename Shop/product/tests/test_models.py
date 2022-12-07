from django.test import TestCase
from ..models import Category, Product, Comment, Property
from customers.tests.test_models import TestCustomerModel


class TestCategory(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Laptop',
            slug='laptop',
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Laptop')
        self.assertEqual(self.category.slug, 'laptop')
        self.assertEqual(self.category.is_sub, False)
        self.assertEqual(self.category.sub_category, None)

    def test_category_str(self):
        self.assertEqual(self.category.__str__(), self.category.name)
        self.assertNotEqual(self.category.__str__(), 'phone')


class TestProduct(TestCase):
    def setUp(self):
        category_test_obj = TestCategory()
        category_test_obj.setUp()
        self.category = category_test_obj.category

        self.product = Product.objects.create(
            name='lenovo ideapad 330',
            slug='lenovo-ideapad-330',
            description='A great laptop with low price',
            price=537,
            stock=12,
        )
        self.product.category.set([self.category])

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'lenovo ideapad 330')
        self.assertEqual(self.product.slug, 'lenovo-ideapad-330')
        self.assertEqual(self.product.description, 'A great laptop with low price')
        self.assertEqual(self.product.price, 537)
        self.assertEqual(self.product.stock, 12)

    def test_product_is_available(self):
        self.assertTrue(self.product.is_available)

    def test_product_str(self):
        self.assertEqual(str(self.product), 'lenovo ideapad 330')


class TestComment(TestCase):
    def setUp(self):
        product_test_obj = TestProduct()
        product_test_obj.setUp()
        self.product = product_test_obj.product

        customer_test_object = TestCustomerModel()
        customer_test_object.setUp()

        customer = customer_test_object.customer

        self.comment = Comment.objects.create(
            customer=customer,
            product=product_test_obj.product,
            title='I recommend it',
            body='This is a great product for programmers',
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.title, 'I recommend it')
        self.assertEqual(self.comment.body, 'This is a great product for programmers')

    def test_comment_str(self):
        self.assertEqual(str(self.comment), f'John Doe commented on lenovo ideapad 330')


class TestProperty(TestCase):
    def setUp(self):
        product_test_obj = TestProduct()
        product_test_obj.setUp()
        self.product = product_test_obj.product

        self.property1 = Property.objects.create(
            key='CPU',
            value='core i7',
        )
        self.property1.product.set([self.product])

        self.property2 = Property.objects.create(
            key='RAM',
            value='16 Gigabytes',
            priority=2
        )
        self.property2.product.set([self.product])

    def test_property_creation(self):
        self.assertEqual(self.property1.key, 'CPU')
        self.assertEqual(self.property1.value, 'core i7')
        self.assertEqual(self.property1.priority, 1)

        self.assertEqual(self.property2.key, 'RAM')
        self.assertEqual(self.property2.value, '16 Gigabytes')
        self.assertEqual(self.property2.priority, 2)

    def test_property_str(self):
        self.assertEqual(str(self.property1), 'CPU:core i7')
        self.assertEqual(str(self.property2), 'RAM:16 Gigabytes')
