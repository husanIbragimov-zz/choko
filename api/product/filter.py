import datetime
import django_filters
from django.db.models import Q
from apps.product.models import Brand, Category, Product, PRODUCT_TYPE, Size
from django.db import models

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
    price_max = django_filters.NumberFilter(label="price_min",lookup_expr="lte")
    price_min = django_filters.NumberFilter(label="price_max",lookup_expr="gte")
    product_type = django_filters.ChoiceFilter(choices=PRODUCT_TYPE, field_name='product_type', lookup_expr='exact')
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    updated_at = django_filters.DateFilter(field_name='updated_at', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['title', 'brand', 'category', 'price_max', 'price_min', 'product_type', 'created_at', 'updated_at']

    def filter_queryset(self, queryset):
        data = self.form.cleaned_data
        data.pop('price_max',None)
        data.pop('price_min',None)
        for name, value in data.items():
            queryset = self.filters[name].filter(queryset, value)
            assert isinstance(
                queryset, models.QuerySet
            ), "Expected '%s.%s' to return a QuerySet, but got a %s instead." % (
                type(self).__name__,
                name,
                type(queryset).__name__,
            )
        return queryset
    