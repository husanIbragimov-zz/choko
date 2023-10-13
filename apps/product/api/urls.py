from .views import AppProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('products', AppProductViewSet, basename='products')

urlpatterns = router.urls
