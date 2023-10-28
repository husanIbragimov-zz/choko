from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, CartItemViewSet, OrderViewSet, WishlistViewSet

router = DefaultRouter()

# router.register('cart', CartViewSet, basename='cart')
# router.register('cart-item', CartItemViewSet, basename='cart-item')
router.register('order', OrderViewSet, basename='order')
# router.register('wishlist', WishlistViewSet, basename='wishlist')

urlpatterns = router.urls
