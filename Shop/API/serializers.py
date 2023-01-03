from rest_framework import serializers
from customers.models import Customer, Address
from product.models import Product


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
