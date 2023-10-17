from django.urls import path
from apps.product.views import about, shop_list, shop_details, index, shop_images, shop_books, shop_clothes, \
    shop_appliances

urlpatterns = [
    path('', index, name="index"),
    path('about/', about, name="about"),
    path('shop/', shop_list, name="products_filter"),
    path('books/', shop_books, name="books"),
    path('clothes/', shop_clothes, name="clothes"),
    path('techniques/', shop_appliances, name="techniques"),
    path('shop-images/', shop_images, name="shop-images"),
    path('shop-details/<int:pk>', shop_details, name="shop-details")
]
