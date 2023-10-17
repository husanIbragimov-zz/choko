from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, BrandViewSet, ColorViewSet, CurrencyViewSet, BannerDiscountViewSet, \
    AdvertisementViewSet, BannerViewSet, SizeViewSet, ProductImageViewSet, ProductViewSet, AdditionalInfoViewSet, \
    RateViewSet, VariantViewSet, AuthorModelViewSet

router = DefaultRouter()

router.register('category', CategoryViewSet, basename='category')
router.register('variant', VariantViewSet, basename='variant')
router.register('brand', BrandViewSet, basename='brand')
router.register('color', ColorViewSet, basename='color')
router.register('currency', CurrencyViewSet, basename='currency')
router.register('sales', BannerDiscountViewSet, basename='banner-discount')
router.register('advertisement', AdvertisementViewSet, basename='advertisement')
router.register('banner', BannerViewSet, basename='banner')
router.register('size', SizeViewSet, basename='size')
router.register('product/image', ProductImageViewSet, basename='product-image')
router.register('product', ProductViewSet, basename='product')
router.register('additional-info', AdditionalInfoViewSet, basename='additional-info')
router.register('rate', RateViewSet, basename='rate')
router.register('author',AuthorModelViewSet)

urlpatterns = router.urls
