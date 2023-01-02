from rest_framework import serializers
from customers.models import Customer


class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ('id', 'full_name', 'user', 'gender', 'age', 'image')

    def get_full_name(self, obj):
        return obj.user.full_name
