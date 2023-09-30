from rest_framework.routers import DefaultRouter

from .views import GetInTouchViewSet

router = DefaultRouter()

router.register('contact', GetInTouchViewSet, basename='contact')


urlpatterns = router.urls
