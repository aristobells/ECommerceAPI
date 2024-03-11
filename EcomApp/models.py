from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from cloudinary_storage.storage import RawMediaCloudinaryStorage

# Create your models here.
class Customer(models.Model):
 user = models.OneToOneField(User, on_delete=models.CASCADE)
 home_address = models.CharField(max_length=50)
 phone_number = models.CharField(max_length=15,blank=True, null=True)
 first_name = models.CharField(max_length=30, blank=True)  # Add first_name directly to Customer model
 last_name = models.CharField(max_length=30, blank=True)
 
 def __str__(self):
  return self.user.username
 
class Category(models.Model):
 slug = models.SlugField(unique=True, blank=True)
 title = models.CharField(max_length=20)
 
 def save(self, *args, **kwargs):
    self.slug = slugify(self.title)
    super().save(*args, **kwargs)
 def __str__(self):
  return self.title
 
class Product(models.Model):
 name = models.CharField(max_length=200)
 category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
 description = models.TextField(blank=True, null=True)
 price = models.DecimalField(max_digits=10, decimal_places=2)
 quantity = models.IntegerField(default=1) #quauantity available
 image = models.ImageField(upload_to='product_images', storage=RawMediaCloudinaryStorage(),null=True,blank=True)
 
 def __str__(self):
  return self.name

class ProductImage(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
  photos = models.ImageField(upload_to='product_images', storage=RawMediaCloudinaryStorage(),null=True,blank=True)

class Cart(models.Model):
 customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
 product = models.ForeignKey(Product, on_delete=models.CASCADE)
 quantity = models.IntegerField()
 
 def __str__(self):
  return f'{self.product.name} for user: {self.customer.user.username}'
 
 class Meta:
  unique_together=('product', 'customer')
 
class Order(models.Model):
 customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
 status = models.BooleanField(db_index=True, default=0)
 total_price = models.DecimalField(max_digits=10, decimal_places=2) # price of all the products in order
 date =models.DateTimeField(db_index=True)
 
class OrderItem(models.Model):
 order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order')
 product = models.ForeignKey(Product, on_delete=models.CASCADE)
 quantity = models.IntegerField()
 price = models.DecimalField(max_digits=10, decimal_places=2)
 
 class Meta:
  unique_together =('order', 'product')
 
class WishList(models.Model):
 customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
 product = models.ForeignKey(Product, on_delete=models.CASCADE)