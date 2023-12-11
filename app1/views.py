from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.utils import timezone
from datetime import timedelta
from django.db.models import F
from django.shortcuts import get_object_or_404
from datetime import datetime

class RegisterUserView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(tokens, status=status.HTTP_201_CREATED)
    
        existing_user = User.objects.filter(username=request.data.get('username')).first()
        if existing_user:
            return Response({'error': 'User already exists'}, status=status.HTTP_409_CONFLICT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
   
    def post(self, request):
        serializer = TokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(tokens, status=status.HTTP_200_OK)
        if 'non_field_errors' in serializer.errors:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)



class VendorListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
        vendors = Vendor.objects.all()
        if not vendors:
            return Response({"error": "No vendors found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendors, many=True)
        return Response({
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorDetailView(APIView): 
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  

    
    def get(self, request, id):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            vendor = Vendor.objects.get(id=id)
            serializer = VendorSerializer(vendor)
            return Response({
                "Vendor_id": vendor.name,
                "data": serializer.data,
            }, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
    

    def put(self, request, id):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            vendor = Vendor.objects.get(id=id)
            serializer = VendorSerializer(vendor, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "Vendor_id": vendor.name,
                    "data": serializer.data,
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            vendor = Vendor.objects.get(id=id)
            vendor.delete()
            return Response({'message': 'Vendor deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    
class PurchaseOrderListCreateView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
        
        vendor_id = request.query_params.get('vendor')

        if vendor_id:
            try:
                purchase_orders = PurchaseOrder.objects.filter(vendor=vendor_id)
                serializer = PurchaseOrderSerializer(purchase_orders, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except PurchaseOrder.DoesNotExist:
                return Response({"error": "Purchase orders not found for this vendor"}, status=status.HTTP_404_NOT_FOUND)
        else:
            purchase_orders = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(purchase_orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
 
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class PurchaseOrderDetailView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    

    def get(self, request, po_number):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            purchase_order = PurchaseOrder.objects.get(po_number=po_number)
            serializer = PurchaseOrderSerializer(purchase_order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)

 
    def put(self, request, po_number):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            purchase_order = PurchaseOrder.objects.get(po_number=po_number)
            serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, po_number):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            purchase_order = PurchaseOrder.objects.get(po_number=po_number)
            purchase_order.delete()
            return Response({'message': 'Purchase order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase order not found'}, status=status.HTTP_404_NOT_FOUND)
               
        
class VendorPerformanceView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
   
    def get(self, request, id):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            vendor = Vendor.objects.get(id=id)
            serializer = PerformanceSerializer(vendor)
            return Response({
                "Vendor_id": vendor.name,
                "data": serializer.data,
            }, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
        
        

class RefreshTokenView(APIView):

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if refresh_token:
            try:
                refresh_token = RefreshToken(refresh_token)
                access_token = str(refresh_token.access_token)
                return Response({'access_token': access_token}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
