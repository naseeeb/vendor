from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    # Add any additional constraints or validators for username here

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')

        # Additional validation if needed
        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")
        
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        
        
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
        
class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')
    