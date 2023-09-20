from rest_framework.routers import DefaultRouter
from .views import AdminViewSet, ClientViewSet

router = DefaultRouter()

router.register('admin', AdminViewSet, basename='admin')
router.register('client', ClientViewSet, basename='client')

urlpatterns = router.urls
