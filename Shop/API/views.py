from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from customers.models import Address
from orders.cart import Cart
from orders.models import Order, OrderItem, Coupon
from product import tasks
from bucket import bucket
from product.models import Product, Category
from .serializers import ProfileSerializer, ProfileUpdateSerializer, AddressSerializer, ProductSerializer, \
    ProductDetailSerializer, CategorySerializer, OrderSerializer, \
    CustomerUnpaidOrdersSerializer, QuantitySerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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


class AddressUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, address_id):
        address = get_object_or_404(Address, customer=request.user.customer, id=address_id)
        serializer = AddressSerializer(instance=address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, address_id):
        address = get_object_or_404(Address, customer=request.user.customer, id=address_id)
        address.delete()
        return Response({'message': 'Address deleted successfully. No content to show'}, status=status.HTTP_200_OK)


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


class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        customer = request.user.customer
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer, product=product)
        result = serializer.data.copy()
        result.update({'message': 'Your comment has been sent successfully.'})
        return Response(result, status=status.HTTP_201_CREATED)


# --------------------- bucket ---------------------
class BucketListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        bucket_data = bucket.get_objects()
        return Response(bucket_data, status=status.HTTP_200_OK)


class BucketDeleteAPIView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, key):
        tasks.delete_object_task.delay(key)
        return Response(status=status.HTTP_200_OK, data={'message': 'object deleted'})


class BucketDownloadAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, key):
        tasks.download_object_task.delay(key)
        return Response(status=status.HTTP_200_OK, data={'message': 'object downloaded'})


class BucketUploadAPIView(APIView):
    permission_classes = [IsAdminUser]

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


# ---------------------------- orders app -----------------------------

class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart(request)
        customer = request.user.customer
        order = Order.objects.create(customer=customer)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        cart.clear()
        serializer = OrderSerializer(instance=order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderCheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        serializer = OrderSerializer(instance=order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderSaveInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        print(request.data)
        serializer = OrderSerializer(instance=order, data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_data = serializer.validated_data
        print(valid_data)
        if valid_data.get('code'):
            coupon = Coupon.objects.get_active_list().filter(code=valid_data['code'])
            if coupon.exists():
                coupon = coupon.get()
                serializer.save(coupon=coupon)
            else:

                return Response({"message": "Error! This Code is used or expired or does not exist."},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save(coupon=None)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderPayAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        if order.is_paid:
            return Response({"message": "Error! This order is paid."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = OrderSerializer(instance=order, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_paid=True)
        order.coupon.deactivate()
        return Response(serializer.data, status=status.HTTP_200_OK)