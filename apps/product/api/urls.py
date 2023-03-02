from django.urls import path, include

urlpatterns = [
    path('api/', include('apps.product.api.v1.urls'))
]
