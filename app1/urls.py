from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    
    path('api/register/', RegisterUserView.as_view(), name='user-register'),
    path('api/login/', LoginUserView.as_view(), name='user-login'),
    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    path('api/vendors/', VendorListCreateView.as_view(), name='vendor-create-list'),
    path('api/vendors/<int:id>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('api/purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-create-list'),
    path('api/purchase_orders/<str:po_number>/', PurchaseOrderDetailView.as_view(), name='purchase-order-detail'),
    
    path('api/vendors/<int:id>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
    
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]
