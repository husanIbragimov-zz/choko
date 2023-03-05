from django.urls import path
from apps.product.views import about, shop_list, IndexView

urlpatterns = [
    path('', IndexView.as_view()),
    path('about/', about),
    path('shop/', shop_list)
]
