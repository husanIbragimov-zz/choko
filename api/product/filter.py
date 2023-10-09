import datetime
import django_filters
from django.db.models import Q
from apps.product.models import Brand, Category, Product, PRODUCT_TYPE, Size


class SizeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='exact')
    product_type = django_filters.ChoiceFilter(choices=PRODUCT_TYPE, field_name='product_type', lookup_expr='exact')

    class Meta:
        model = Size
        fields = ['name', 'product_type']


class BrandFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='exact')
    product_type = django_filters.ChoiceFilter(choices=PRODUCT_TYPE, field_name='product_type', lookup_expr='exact')

    class Meta:
        model = Brand
        fields = ['title', 'product_type']


class CategoryFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='exact')
    product_type = django_filters.ChoiceFilter(choices=PRODUCT_TYPE, field_name='product_type', lookup_expr='exact')

    class Meta:
        model = Category
        fields = ['title', 'product_type']


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    brand = django_filters.ModelChoiceFilter(queryset=Brand.objects.all())
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    price = django_filters.RangeFilter()
    product_type = django_filters.ChoiceFilter(choices=PRODUCT_TYPE, field_name='product_type', lookup_expr='exact')
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    updated_at = django_filters.DateFilter(field_name='updated_at', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['title', 'brand', 'category', 'price', 'product_type', 'created_at', 'updated_at']

