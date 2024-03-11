from django.urls import path
from . import views
urlpatterns = [
  path('',views.ProductView.as_view(), name = "product"),
  path('customer/<int:pk>',views.SingleCustomerView.as_view(), name = "single-customer"),
 path('category',views.CategoryView.as_view(), name = "category"),
 path('category/<int:pk>',views.SingleCategoryView.as_view(), name = "single-category"),
 path('product',views.ProductView.as_view(), name = "product"),
 path('product/<int:pk>',views.SingleProductView.as_view(), name = "single-product"),
 path('cart',views.CartView.as_view(), name = "cart"),
 path('order',views.OrderView.as_view(), name = "order"),
 path('order/<int:pk>',views.SingleOrderView.as_view(), name = "single-order"),
 path('wishlist', views.WishListView.as_view(), name ="wishlist")
 # path('product/<int:pk>',views.ProductRetrieveUpdateDestroyAPIview.as_view(), name = "retrieve_update_destroy_product"),
]