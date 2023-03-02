from django.urls import path, include

urlpatterns = [
    path('api/', include('apps.account.api.v1.urls'))
]
