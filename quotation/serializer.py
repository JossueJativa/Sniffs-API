from rest_framework import serializers
from .models import QuotationHeader, QuotationDetail

class QuotationHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationHeader
        fields = '__all__'

class QuotationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationDetail
        fields = '__all__'