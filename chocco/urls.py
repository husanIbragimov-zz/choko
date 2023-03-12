"""chocco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from apps.base import views
from apps.base.views import set_language

urlpatterns = [
    path('admin/', admin.site.urls),

] + i18n_patterns(
    # language
    path('i18n/', include('django.conf.urls.i18n')),
    # lib
    path('base/', include('allauth.urls')),

    # local apps
    path('', include('apps.product.urls')),
    path('about/', include('apps.about.api.urls')),
    path('order/', include('apps.order.urls')),
    path('contact/', include('apps.contact.api.urls')),

    # login & register
    path('register/', views.register, name="register"),
    path('login/', views.login_func, name="login"),
    path('logout/', views.logout_func, name="logout"),
    prefix_default_language=False,
)



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
