from django.urls import path
from apps.product.views import about, shop_list, IndexView, shop_details

urlpatterns = [
    path('', IndexView.as_view()),
    path('about/', about),
    path('shop/', shop_list),
    path('shop-details/<int:id>', shop_details, name="shop-details")
]
