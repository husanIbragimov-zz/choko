import django_filters
from django.db import models
from apps.order.models import Order, Cart, CartItem, Wishlist
from django.contrib.auth.models import User


class OrderFilter(django_filters.FilterSet):
    user  = django_filters.ModelChoiceFilter(queryset = User.objects.all())
    phone_number = django_filters.CharFilter(field_name="phone_number",lookup_expr="icontains")
    status = django_filters.ChoiceFilter(choices = Order.STATUS,field_name = "status")
    class Meta:
        models = Order
        fields = ('user',"phone_number",'status')