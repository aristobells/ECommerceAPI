from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import  generics, status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.decorators import permission_classes
from .serializers import CustomerSerialzer, CategorySerializer,CreateProductSerializer, ListProductSerializer,CartSerializer,OrderSerializer,OrderItemSerializer, WishListSerializer, CreateWishListSerializer
from .models import Customer, Category, Product, Cart, Order,OrderItem, WishList
from datetime import datetime
from decimal import Decimal
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.
# Customized permission class ===================================================================================
class IsmanagerOrSuperUser(BasePermission):
  def has_permission(self, request, view):
    return request.user.groups.filter(name ='manager').exists() or request.user.is_superuser
    
# END of Customized permission class ============================================================================

# Viwes for Customers ===========================================================================================
class SingleCustomerView(generics.RetrieveUpdateAPIView):
  queryset = Customer.objects.all()
  permission_classes = [IsAuthenticated]
  serializer_class = CustomerSerialzer
  # End of Customer views ======================================================================================
  
# Viwes for Category ===========================================================================================
class CategoryView(generics.ListCreateAPIView):
  permission_classes = [IsAuthenticated]
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  
  def post(self, request, *args, **kwargs):
    if self.request.user.groups.filter(name='manager').exists():
      serialized_item = CategorySerializer(data=request.data)
      serialized_item.is_valid(raise_exception=True)
      serialized_item.save()
      return Response({'message':'Category created successfully!!!'}, status.HTTP_201_CREATED)
    else:
      return Response({'message': 'You are not allowed to create category'}, status.HTTP_403_FORBIDDEN)
    
class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
  permission_classes =[IsAuthenticated,IsmanagerOrSuperUser]
  queryset = Category.objects.all()
  serializer_class = CategorySerializer  
  
  def delete(self, request, *args, **kwargs):
    instance = self.get_object()
    instance.delete()
    return Response({"message": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
# Viwes for Category ===========================================================================================

# Product views ================================================================================================
class ProductView(generics.ListCreateAPIView):
  queryset = Product.objects.all()
  serializer_class = CreateProductSerializer
  parser_classes = [MultiPartParser, FormParser]
  
  def post(self, request, *args, **kwargs):
    serialized_item = CreateProductSerializer(data=request.data)
    serialized_item.is_valid(raise_exception=True)
    serialized_item.save()
    return Response({'message': 'Product created sucessfully'})
  
  def get(self, request, *args, **kwargs):
    item = Product.objects.select_related('category').all()
    serialized_item = ListProductSerializer(item, many=True)
    return Response(serialized_item.data)
  
  def get_permissions(self):
    permission_classes = []
    if self.request.method != 'GET':
      permission_classes = [IsmanagerOrSuperUser]
    return [permission() for permission in permission_classes]
  
class SingleProductView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Product.objects.all()
  serializer_class = CreateProductSerializer
  
  def get(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = ListProductSerializer(instance)
    return Response(serializer.data)
  
  
  def get_permissions(self):
    permission_classes = []
    if self.request.method != 'GET':
      permission_classes = [IsmanagerOrSuperUser]
    return [permission() for permission in permission_classes]
  
  def update(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    return Response(serializer.data)
# End of Product views ================================================================================================

# Cart views ==========================================================================================================
class CartView(generics.ListCreateAPIView):
  permission_classes = [IsAuthenticated]
  queryset = Cart.objects.all()
  serializer_class = CartSerializer
  
  def get_queryset(self):
    return Cart.objects.all().filter(customer = self.request.user.customer)
  print('Accessing customer\'s profile')
  def post(self, request, *args, **kwargs):
    data = request.data
    curent_userID = self.request.user.customer.id
    if self.request.user.customer.id == int(data['customer']):
      print('This cart belongs to the current customer')
      serialized_item = CartSerializer(data=request.data)
      serialized_item.is_valid(raise_exception=True)
      serialized_item.save()
      return Response({'message': 'Added to Cart'}, status= status.HTTP_200_OK)
    return Response({'message':'Unauthorized  Cart creation'}, status=status.HTTP_401_UNAUTHORIZED)
  def delete(self, request, *args, **kwargs):
    Cart.objects.all().filter(customerr=self.request.user.customer).delete()
    return Response("ok")
# END of Cart views =============================================================================================
# Order Views ===================================================================================================
class OrderView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    ordering_fields=['status','total_price', 'date']
    
    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.all().filter(customer=self.request.user.customer)

    def create(self, request, *args, **kwargs):
        cart_items = Cart.objects.all().filter(customer=self.request.user.customer)
        product_count = cart_items.count()
        if product_count == 0:
            return Response({'message': 'No item in the cart'})  
        today = datetime.today()
        today_str = today.strftime('%Y-%m-%d')
        customer = self.request.user.customer
        total = self.get_total_price(self.request.user.customer) 
        order = Order.objects.create(customer=customer,total_price=total,date=today_str)
        order_items=[]
        for cart_item in cart_items:
          order_item = OrderItem(
              order = order,
              product = cart_item.product,
              quantity = cart_item.quantity,
              price = cart_item.product.price 
          )
          order_items.append(order_item)
        OrderItem.objects.bulk_create(order_items)
        cart_items.delete()
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    def get_total_price(self, customer):
        items = Cart.objects.all().filter(customer=customer)
        total = Decimal('0.0') 
        for item in items:
            total += item.product.price
        return total
      
class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = [IsmanagerOrSuperUser]
  queryset = Order.objects.all()
  serializer_class = OrderSerializer
# END of Order Views ============================================================================================
# WishList Views ================================================================================================
class WishListView(generics.ListCreateAPIView):
  permission_classes = [IsAuthenticated]
  # queryset = WishList.objects.all()
  serializer_class = CreateWishListSerializer
  
  def get_queryset(self):
    if self.request.user.groups.filter(name ='manager').exists() or self.request.user.is_superuser:
      return WishList.objects.all()
    else:
      return WishList.objects.all().filter(customer=self.request.user.customer)
# END of  WishList Views ========================================================================================