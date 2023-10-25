import datetime
import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q
from apps.product.models import Brand, Category, Product, PRODUCT_TYPE, Size, Author, Color, ProductImage


class AppProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all())
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.filter(parent__isnull=False))
    product_type = django_filters.ChoiceFilter(choices=PRODUCT_TYPE, field_name='product_type', lookup_expr='exact')
    author = django_filters.ModelChoiceFilter(queryset=Author.objects.all(), field_name='author', lookup_expr='exact')
    size = django_filters.ModelMultipleChoiceFilter(queryset=Size.objects.all())

    class Meta:
        model = Product
        fields = ['title', 'category', 'brand', 'size', 'author', 'product_type']
