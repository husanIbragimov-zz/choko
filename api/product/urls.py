from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, BrandViewSet, ColorViewSet, CurrencyViewSet, BannerDiscountViewSet, \
    AdvertisementViewSet

router = DefaultRouter()

router.register('category', CategoryViewSet, basename='category')
router.register('brand', BrandViewSet, basename='brand')
router.register('color', ColorViewSet, basename='color')
router.register('currency', CurrencyViewSet, basename='currency')
router.register('sales', BannerDiscountViewSet, basename='banner-discount')
router.register('advertisement', AdvertisementViewSet, basename='advertisement')

urlpatterns = router.urls
