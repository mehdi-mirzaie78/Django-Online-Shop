from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProfileSerializer, ProfileUpdateSerializer, AddressSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


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
