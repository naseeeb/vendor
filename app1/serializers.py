from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.db.models import Avg, F

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)


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
    on_time_delivery_rate = serializers.SerializerMethodField()
    quality_rating_avg = serializers.SerializerMethodField()
    average_response_time = serializers.SerializerMethodField()
    fulfillment_rate = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        fields = ('on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')

    def get_on_time_delivery_rate(self, vendor):
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        total_completed_pos = completed_pos.count()
        if total_completed_pos == 0:
            return 0.0
        on_time_delivered_pos = completed_pos.filter(delivery_date__lte=F('acknowledgment_date'))
        return on_time_delivered_pos.count() / total_completed_pos

    def get_quality_rating_avg(self, vendor):
        quality_ratings = PurchaseOrder.objects.filter(vendor=vendor, quality_rating__isnull=False)
        return quality_ratings.aggregate(avg_rating=Avg('quality_rating')).get('avg_rating', 0.0)

    def get_average_response_time(self, vendor):
        all_pos = PurchaseOrder.objects.filter(vendor=vendor)
        response_times = [(po.acknowledgment_date - po.issue_date).total_seconds()
                          for po in all_pos if po.acknowledgment_date]
        if not response_times:
            return 0.0
        return sum(response_times) / len(response_times) / 3600  # Convert to hours

    def get_fulfillment_rate(self, vendor):
        all_pos = PurchaseOrder.objects.filter(vendor=vendor)
        successfully_fulfilled_pos = all_pos.filter(status='completed')
        total_pos_count = all_pos.count()
        if total_pos_count == 0:
            return 0.0
        return successfully_fulfilled_pos.count() / total_pos_count