from django.db import models 
from django.db.models import Count, Avg
from datetime import timedelta
from django.contrib.auth.models import User


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0) 

    def calculate_on_time_delivery_rate(self):
        completed_orders = self.purchaseorder_set.filter(
            status='completed',
            delivery_date__lte=models.F('acknowledgment_date')
        ).count()

        total_completed_orders = self.purchaseorder_set.filter(status='completed').count()

        if total_completed_orders > 0:
            return completed_orders / total_completed_orders
        return 0

    def calculate_quality_rating_avg(self):
        completed_orders = self.purchaseorder_set.filter(
            status='completed', quality_rating__isnull=False
        )
        if completed_orders.exists():
            return completed_orders.aggregate(Avg('quality_rating'))['quality_rating__avg']
        return 0

    def calculate_average_response_time(self):
        completed_orders = self.purchaseorder_set.filter(acknowledgment_date__isnull=False)
        response_times = [(po.acknowledgment_date - po.issue_date).days for po in completed_orders]

        if response_times:
            return sum(response_times) / len(response_times)
        return 0

    def calculate_fulfillment_rate(self):
        total_orders = self.purchaseorder_set.count()
        successful_orders = self.purchaseorder_set.filter(
            status='completed', quality_rating__isnull=False
        ).count()

        if total_orders > 0:
            return successful_orders / total_orders
        return 0

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po_number = models.CharField(max_length=50, unique=True)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()  # Details of items ordered
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO {self.po_number} for {self.vendor.name}"


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"Performance of {self.vendor.name} on {self.date}"


