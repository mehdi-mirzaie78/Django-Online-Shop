from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from orders.cart import Cart
from product import tasks
from bucket import bucket
from product.models import Product, Category
from .serializers import ProfileSerializer, ProfileUpdateSerializer, AddressSerializer, ProductSerializer, \
    ProductDetailSerializer, CategorySerializer, OrderSerializer, \
    CustomerUnpaidOrdersSerializer, QuantitySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status


# --------------------- accounts app ---------------------
class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = request.user.customer
        serializer = ProfileSerializer(instance=customer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        customer = user.customer
        serializer = ProfileUpdateSerializer(instance=customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user.full_name = serializer.validated_data['full_name']
        user.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# --------------------- customers app ---------------------
class AddressListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = request.user.customer
        addresses = customer.addresses.all()
        serializer = AddressSerializer(instance=addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        customer = request.user.customer
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# --------------------- product app ---------------------
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(is_sub=False)
    serializer_class = CategorySerializer


class ProductListAPIView(APIView):

    def get(self, request):
        products = Product.objects.filter(is_available=True)
        serializer = ProductSerializer(instance=products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailAPIView(APIView):

    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        serializer = ProductDetailSerializer(instance=product)
        return Response(serializer.data, status=status.HTTP_200_OK)


# --------------------- bucket ---------------------
class BucketListAPIView(APIView):

    def get(self, request):
        bucket_data = bucket.get_objects()
        return Response(bucket_data, status=status.HTTP_200_OK)


class BucketDeleteAPIView(APIView):
    def delete(self, request, key):
        tasks.delete_object_task.delay(key)
        return Response(status=status.HTTP_200_OK, data={'message': 'object deleted'})


class BucketDownloadAPIView(APIView):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        return Response(status=status.HTTP_200_OK, data={'message': 'object downloaded'})


class BucketUploadAPIView(APIView):
    def get(self, request, key):
        tasks.upload_object_task.delay(key)
        return Response(status=status.HTTP_200_OK, data={'message': 'object uploaded'})


# --------------------- cart ---------------------

class CartAPIView(APIView):

    def get(self, request):
        cart = Cart(request)
        result = cart.cart.copy()
        if request.user.is_authenticated:
            customer = request.user.customer
            serializer = CustomerUnpaidOrdersSerializer(instance=customer)
            result.update(serializer.data)
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        serializer = QuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if cart.add(product=product, quantity=serializer.validated_data['quantity']):
            return Response(data=cart.cart, status=status.HTTP_200_OK)
        return Response(data={'message': 'product is not available'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        if cart.remove(product=product):
            return Response(data={'message': 'product removed from cart'}, status=status.HTTP_200_OK)
        return Response(data={'message': 'product is not in your cart'}, status=status.HTTP_400_BAD_REQUEST)