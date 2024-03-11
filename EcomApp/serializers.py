from rest_framework import serializers
from .models import Customer, Category, Product, Cart, OrderItem, Order, WishList, ProductImage
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
 class Meta:
  model = User
  fields = ['username']

class CustomerSerialzer(serializers.ModelSerializer):
 user = UserSerializer(read_only=True)
 class Meta:
  model = Customer
  fields = ['home_address', 'phone_number', 'first_name', 'last_name', 'user']

class  CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = "__all__"
    
class ProductImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = ProductImage
    fields = "__all__"
    
class CreateProductSerializer(serializers.ModelSerializer):
  uploaded_images = serializers.ListField(
    child = serializers.ImageField(max_length=1000000, allow_empty_file = False, use_url =False), write_only = True
  )
  class Meta:
    model = Product
    fields = ["name","description",'price','quantity','image','category','uploaded_images' ]
    
  def create(self, validated_data):
    uploaded_images = validated_data.pop('uploaded_images', [])
    product = Product.objects.create(**validated_data)
    for image in uploaded_images:
        ProductImage.objects.create(product=product, photos=image)
    return product

    
class ListProductSerializer(serializers.ModelSerializer):
  images = ProductImageSerializer(many=True, required=False)
  category = serializers.StringRelatedField()
  class Meta:
    model = Product
    fields = ["name","description",'price','quantity','image','images','category' ]

    
class CartSerializer(serializers.ModelSerializer):
  # customer = serializers.PrimaryKeyRelatedField(
  #   queryset = get_user_model().objects.all(),
  #   default=serializers.CurrentUserDefault(),
  # )
  price = serializers.SerializerMethodField()
  total_price = serializers.SerializerMethodField()

  def get_total_price(self, Cart):
    return Cart.product.price * Cart.quantity
  def get_price(self, Cart):
    return Cart.product.price
    

  class Meta:
    model = Cart
    fields = ['customer','product', 'quantity','price','total_price']
    
    extra_kwargs = {
          'total_price': {'read_only': True},
          'price' : {'read_only': True},
      }

class OrderItemSerializer(serializers.ModelSerializer):
  product = serializers.StringRelatedField()
  class Meta:
    model = OrderItem
    fields = ['order', 'product', 'quantity', 'price']
  
  
class OrderSerializer(serializers.ModelSerializer):
  orderitem = OrderItemSerializer(many=True, read_only=True, source='order' )
  total_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
  date = serializers.DateTimeField(read_only=True)
  class Meta:
    model = Order
    fields = ['customer','status', 'total_price', 'date', 'orderitem']

class WishListSerializer(serializers.ModelSerializer):
  product = serializers.StringRelatedField()
  customer = serializers.StringRelatedField()
  class Meta:
    model = WishList
    fields = ['customer', 'product']
    
class CreateWishListSerializer(serializers.ModelSerializer):
  class Meta:
    model = WishList
    fields = "__all__"