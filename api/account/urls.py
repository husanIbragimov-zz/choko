from rest_framework.routers import DefaultRouter
from .views import AdminViewSet, ClientViewSet, LoginAPIView
from django.urls import path

router = DefaultRouter()

router.register('admin', AdminViewSet, basename='admin')
router.register('client', ClientViewSet, basename='client')

urlpatterns = [
    path('login/', LoginAPIView.as_view())
]+router.urls
