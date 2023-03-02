from django.urls import path, include

urlpatterns = [
    path('api/', include('apps.contact.api.v1.urls'))
]
