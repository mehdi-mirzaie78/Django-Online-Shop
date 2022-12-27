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
        self.assertEqual(str(self.category), 'Laptop')
        self.assertNotEqual(str(self.category), 'phone')

    def test_category_get_absolute_url(self):
        self.assertEqual(self.category.get_absolute_url(), '/category/laptop/')


class TestProperty(TestCase):
    def setUp(self):
        self.property1 = Property.objects.create(
            key='CPU',
            value='core i7',
        )

        self.property2 = Property.objects.create(
            key='RAM',
            value='16 Gigabytes',
            priority=2
        )
        # self.property2.product.set([self.product])

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


class TestProduct(TestCase):
    def setUp(self):
        category_test_obj = TestCategory()
        category_test_obj.setUp()
        self.category = category_test_obj.category

        property_test_obj = TestProperty()
        property_test_obj.setUp()
        self.property1 = property_test_obj.property1
        self.property2 = property_test_obj.property2

        self.product = Product.objects.create(
            name='lenovo ideapad 330',
            slug='lenovo-ideapad-330',
            description='A great laptop with low price',
            price_no_discount=1000,
            price=900,
            stock=12,
        )
        self.product.category.set([self.category])
        self.product.properties.set([self.property1, self.property2])

        self.product2 = Product.objects.create(
            name='msi',
            slug='msi',
            description='A great laptop with great price',
            price_no_discount=1000,
            price=900,
            stock=12,
        )
        self.product2.category.set([self.category])
        self.product2.properties.set([self.property1, self.property2])

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'lenovo ideapad 330')
        self.assertEqual(self.product.slug, 'lenovo-ideapad-330')
        self.assertEqual(self.product.description, 'A great laptop with low price')
        self.assertEqual(self.product.price_no_discount, 1000)
        self.assertEqual(self.product.discount, 0)
        self.assertEqual(self.product.price, 1000)
        self.assertEqual(self.product.stock, 12)
        self.assertTrue(self.product.is_available)

    def test_product_save(self):
        self.product.stock = 0
        self.product.discount = 10
        self.product.save()

        self.assertFalse(self.product.is_available)
        self.assertEqual(self.product.discount, 10)
        self.assertEqual(self.product.price, 900)

    def test_product_str(self):
        self.assertEqual(str(self.product), 'lenovo ideapad 330')
        self.assertNotEqual(str(self.product), 'ideapad 330')

    def test_product_image_tage(self):
        self.assertEqual(self.product.image_tag(), '<img src="/media/default/product.png" width="250" height="250" />')
        self.assertNotEqual(self.product.image_tag(), None)


class TestComment(TestCase):
    def setUp(self):
        product_test_obj = TestProduct()
        product_test_obj.setUp()
        self.product = product_test_obj.product

        customer_test_object = TestCustomerModel()
        customer_test_object.setUp()
        self.customer = customer_test_object.customer

        self.comment = Comment.objects.create(
            customer=self.customer,
            product=self.product,
            title='I recommend it',
            body='This is a great product for programmers',
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.title, 'I recommend it')
        self.assertEqual(self.comment.body, 'This is a great product for programmers')
        self.assertEqual(self.comment.customer, self.customer)
        self.assertEqual(self.comment.product, self.product)

    def test_comment_str(self):
        self.assertEqual(str(self.comment), 'John Snow commented on lenovo ideapad 330')
        self.assertNotEqual(str(self.comment), None)
