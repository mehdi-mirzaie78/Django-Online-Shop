from rest_framework import serializers
from customers.models import Customer, Address
from orders.models import Order
from product.models import Product, Category


# --------------------- accounts app ---------------------
class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    phone_number = serializers.CharField(max_length=13, required=False, read_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'user', 'full_name', 'phone_number', 'gender', 'age', 'image')

    def get_full_name(self, obj):
        return obj.user.full_name

    def get_phone_number(self, obj):
        return obj.user.phone_number


class ProfileUpdateSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Customer
        fields = ('id', 'full_name', 'user', 'gender', 'age', 'image')


# --------------------- customers app ---------------------
class AddressSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Address
        fields = ('id', 'customer', 'city', 'body', 'postal_code')


# --------------------- product app ---------------------
class CategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'is_sub', 'sub_categories')

    def get_sub_categories(self, obj):
        return CategorySerializer(obj.scategory.all(), many=True).data


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'image', 'description', 'price_no_discount', 'discount', 'price', 'is_available')


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True, many=True)
    properties = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'category', 'properties', 'slug', 'image', 'description',
            'price_no_discount', 'discount', 'price', 'is_available')


# --------------------- orders app ---------------------
class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = (
            "id", "customer", "is_paid", "discount", "city", "body", "postal_code", "phone_number", "status", "coupon",
            "transaction_code",
        )


class QuantitySerializer(serializers.Serializer):
    quantity = serializers.IntegerField()

    def validate_quantity(self, value):
        if value < 1 or value > 2:
            raise serializers.ValidationError("Quantity must be greater than 0 and lower than 3")
        return value


class CustomerUnpaidOrdersSerializer(serializers.ModelSerializer):
    unpaid_orders = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ('id', 'unpaid_orders')

    def get_unpaid_orders(self, obj):
        if obj:
            unpaid_orders = obj.orders.filter(is_paid=False)
            result = OrderSerializer(unpaid_orders, many=True).data
        else:
            result = {'unpaid_orders': None}
        return result
