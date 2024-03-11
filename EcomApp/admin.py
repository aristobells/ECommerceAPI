from django.contrib import admin
from .models import Category, Product, Customer,Cart,Order,OrderItem,WishList,ProductImage
# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(WishList)
admin.site.register(ProductImage)