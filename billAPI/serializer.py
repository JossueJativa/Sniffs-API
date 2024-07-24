from .models import BillHeader, BillDetail
from rest_framework import serializers

class BillHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillHeader
        fields = '__all__'

class BillDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillDetail
        fields = '__all__'