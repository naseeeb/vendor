from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import permissions




urlpatterns = [
    
    path('api/register/', RegisterUserView.as_view(), name='user-register'),
    path('api/login/', LoginUserView.as_view(), name='user-login'),
    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    path('api/vendors/', VendorListCreateView.as_view(), name='vendor-create-list'),
    path('api/vendors/<int:id>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('api/purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-create-list'),
    path('api/purchase_orders/<str:po_number>/', PurchaseOrderDetailView.as_view(), name='purchase-order-detail'),
    
    path('api/vendors/<int:id>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
    
    
   

]
