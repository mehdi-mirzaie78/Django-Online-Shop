from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = request.user.customer
        serializer = ProfileSerializer(instance=customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
