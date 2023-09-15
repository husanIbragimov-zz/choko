from .serializers import CategoryListSerializer, CategoryCreateSerializer, BrandSerializer, ColorSerializer, \
    CurrencySerializer, BannerDiscountSerializer, AdvertisementSerializer
from apps.product.models import Category, Brand, Color, Currency, BannerDiscount, Advertisement
from rest_framework import generics, viewsets, views, mixins, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                      mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = CategoryListSerializer
    ordering_fields = ['created_at']
    queryset = Category.objects.all()

    def get_queryset(self):
        return Category.objects.filter(is_active=True).order_by('title')

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return CategoryCreateSerializer
        if self.action == 'parents':
            return CategoryCreateSerializer
        return CategoryListSerializer

    @action(methods=['get'], detail=False)
    def parents(self, request, *args, **kwargs):
        parents = self.get_queryset().filter(parent__isnull=True)
        serializer = self.get_serializer(parents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(parent__isnull=True))

        page = self.paginate_queryset(queryset)
        if page is not None:
            sz = self.get_serializer(page, many=True)
            return self.get_paginated_response(sz.data)
        sz = self.get_serializer(queryset, many=True)
        return Response(sz.data)


class BrandViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                   mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = BrandSerializer
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Brand.objects.all().order_by('title')


class ColorViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                   mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = ColorSerializer
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Color.objects.all().order_by('title')


class CurrencyViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                      mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = CurrencySerializer
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Currency.objects.all().order_by('-id')


class BannerDiscountViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                            mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = BannerDiscountSerializer
    ordering_fields = ['created_at']

    def get_queryset(self):
        return BannerDiscount.objects.all().order_by('-id')


class AdvertisementViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                           mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = AdvertisementSerializer
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Advertisement.objects.all().order_by('-id')
