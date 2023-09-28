from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('book', BookModelViewSet, basename='book')
router.register('author', AuthorModelViewSet, basename='author')
router.register('printed', PrintedModelViewSet, basename='printed')
router.register('image', ProductImageModelViewSet, basename='category')

urlpatterns = [
]
urlpatterns += router.urls