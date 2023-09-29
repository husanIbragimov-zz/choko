from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import CategoryListSerializer, CategoryCreateSerializer, BrandSerializer, ColorSerializer, \
    CurrencySerializer, BannerDiscountSerializer, AdvertisementSerializer, BannerSerializer, SizeSerializer, \
    ProductImageCreateSerializer, ProductImageListSerializer, ProductCreateSerializer, ProductDetailSerializer, \
    ProductListSerializer, AdditionalInfoListSerializer, AdditionalInfoCreateSerializer, RateCreateSerializer, \
    RateListSerializer, VariantSerializer
from apps.product.models import Category, Brand, Color, Currency, BannerDiscount, Advertisement, Banner, Size, \
    ProductImage, Product, AdditionalInfo, Rate
from apps.base.models import Variant
from api.account.permissions import IsSuperUser
from rest_framework import viewsets, mixins, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                      mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = CategoryListSerializer
    ordering_fields = ['created_at']
    queryset = Category.objects.all()
    permission_classes = [IsSuperUser]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Category.objects.filter(is_active=True).order_by('-id')

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

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsSuperUser | permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class VariantViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = VariantSerializer
    ordering_fields = ['created_at']
    queryset = Variant.objects.all()
    permission_classes = [IsSuperUser]

    def get_queryset(self):
        return Category.objects.filter(is_active=True).order_by('-id')


class BrandViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = BrandSerializer
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Brand.objects.all().order_by('title')

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsSuperUser | permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class ColorViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = ColorSerializer
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Color.objects.all().order_by('title')

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsSuperUser | permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class CurrencyViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                      mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = CurrencySerializer
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Currency.objects.all().order_by('-id')

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsSuperUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class BannerDiscountViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                            mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = BannerDiscountSerializer
    ordering_fields = ['created_at']
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return BannerDiscount.objects.all().order_by('-id')

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsSuperUser | permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class AdvertisementViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                           mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = AdvertisementSerializer
    ordering_fields = ['created_at']
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Advertisement.objects.all().order_by('-id')

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsSuperUser | permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class BannerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = BannerSerializer
    ordering_fields = ['created_at']
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Banner.objects.all().order_by('-id')

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [permissions.IsAdminUser | IsSuperUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class SizeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = SizeSerializer
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Size.objects.all().order_by('-id')

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [permissions.IsAdminUser | IsSuperUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]




class ProductImageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                          mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = ProductImageListSerializer
    ordering_fields = ['created_at']
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return ProductImage.objects.all().order_by('-id')

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return ProductImageCreateSerializer
        return ProductImageListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(product__is_active=True))

        page = self.paginate_queryset(queryset)
        if page is not None:
            sz = self.get_serializer(page, many=True)
            return self.get_paginated_response(sz.data)
        sz = self.get_serializer(queryset, many=True)
        return Response(sz.data)
    


    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsSuperUser | permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = ProductListSerializer
    ordering_fields = ['created_at']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'brand', 'size', 'banner_discount']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Product.objects.filter(
            Q(is_active=True) & Q(Q(product_type='clothing') | Q(product_type='product'))).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return ProductCreateSerializer
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(is_active=True))
        page = self.paginate_queryset(queryset)
        if page is not None:
            sz = self.get_serializer(page, many=True)
            return self.get_paginated_response(sz.data)
        sz = self.get_serializer(queryset, many=True)
        return Response(sz.data)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        sz_ = ProductCreateSerializer(data=data)
        sz_.is_valid(raise_exception=True)
        sz_.save()
        images = {

        }
        files = request.FILES
        product_type  = data
        for file in files:
            images[file] = []
            for i in files.getlist(file):
                sz = ProductImageCreateSerializer(data={'image': i, 'color': int(file), 'product': sz_.data['id'],
                                               'price': data[f'price_{str(file)}']})
                sz.is_valid(raise_exception=True)
                sz.save()
                images[file].append(sz.data)

        return Response({'data': sz_.data, 'images': images}, status=status.HTTP_201_CREATED)


    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsSuperUser | permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class AdditionalInfoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                            mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = AdditionalInfoListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['created_at']
    search_fields = ['title']

    def get_queryset(self):
        return AdditionalInfo.objects.filter(product__is_active=True).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return AdditionalInfoCreateSerializer
        return AdditionalInfoListSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsSuperUser | permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class RateViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = RateListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['created_at']
    search_fields = ['rate', 'comment']
    permission_classes = []

    def get_queryset(self):
        return Rate.objects.filter(product__is_active=True).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return RateCreateSerializer
        return RateListSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsSuperUser | permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
