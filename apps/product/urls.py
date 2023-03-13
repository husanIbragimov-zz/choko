from django.urls import path
from apps.product.views import about, shop_list, shop_details, index

urlpatterns = [
    path('', index, name="index"),
    path('about/', about),
    path('shop/', shop_list, name="products_filter"),
    path('shop-details/<int:id>', shop_details, name="shop-details")
]
