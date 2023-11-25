from django.db.models import Q, Min,F,ExpressionWrapper, fields
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from api.book.helper import LargeResultsSetPagination
from .serializers import AuthorSerializer, ProductImageSZ
from .filter import BrandFilter, CategoryFilter, ProductFilter, SizeFilter
from api.book.serializers import BookImageSerializer
from django.db.models import Value, FloatField
from django.db.models.expressions import RawSQL

from .serializers import CategoryListSerializer, CategoryCreateSerializer, BrandSerializer, ColorSerializer, \
    CurrencySerializer, BannerDiscountSerializer, AdvertisementSerializer, BannerSerializer, SizeSerializer, \
    ProductImageCreateSerializer, ProductImageListSerializer, ProductCreateSerializer, ProductDetailSerializer, \
    ProductListSerializer, AdditionalInfoListSerializer, AdditionalInfoCreateSerializer, RateCreateSerializer, \
    RateListSerializer, VariantSerializer
from apps.product.models import Author, Category, Brand, Color, Currency, BannerDiscount, Advertisement, Banner, Size, \
    ProductImage, Product, AdditionalInfo, Rate
from apps.base.models import Variant
from api.account.permissions import IsSuperUser
from rest_framework import viewsets, mixins, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                      mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = CategoryListSerializer
    ordering_fields = ['created_at']
    queryset = Category.objects.all()
    permission_classes = [IsSuperUser]
    parser_classes = [MultiPartParser, FormParser]
    filterset_class = CategoryFilter
    pagination_class = None

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
        queryset = self.filter_queryset(
            self.get_queryset().filter(parent__isnull=True))

        page = self.paginate_queryset(queryset)
        if page is not None:
            sz = self.get_serializer(page, many=True)
            return self.get_paginated_response(sz.data)
        sz = self.get_serializer(queryset, many=True)
        return Response(sz.data)

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            # permission_classes = [IsSuperUser | permissions.IsAdminUser]
            permission_classes = [permissions.AllowAny]

        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class VariantViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = VariantSerializer
    ordering_fields = ['created_at']
    queryset = Variant.objects.all()
    permission_classes = [IsSuperUser]
    pagination_class = None

    def get_queryset(self):
        return self.queryset.order_by('-id')


class BrandViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = BrandSerializer
    ordering_fields = ['created_at']
    filterset_class = BrandFilter
    pagination_class = None

    def get_queryset(self):
        return Brand.objects.all().order_by('title')

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            # permission_classes = [IsSuperUser | permissions.IsAdminUser]
            permission_classes = [permissions.AllowAny]

        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class ColorViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = ColorSerializer
    ordering_fields = ['created_at']
    pagination_class = None

    def get_queryset(self):
        return Color.objects.all().order_by('title')

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            # permission_classes = [IsSuperUser | permissions.IsAdminUser]
            permission_classes = [permissions.AllowAny]

        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class CurrencyViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                      mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = CurrencySerializer
    ordering_fields = ['created_at']
    pagination_class = None

    def get_queryset(self):
        return Currency.objects.all().order_by('-id')

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            # permission_classes = [IsSuperUser]
            permission_classes = [permissions.AllowAny]

        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class BannerDiscountViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                            mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = BannerDiscountSerializer
    ordering_fields = ['created_at']
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = None

    def get_queryset(self):
        return BannerDiscount.objects.all().order_by('-id')

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            # permission_classes = [IsSuperUser | permissions.IsAdminUser]
            permission_classes = [permissions.AllowAny]

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
            # permission_classes = [IsSuperUser | permissions.IsAdminUser]
            permission_classes = [permissions.AllowAny]

        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class BannerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = BannerSerializer
    ordering_fields = ['created_at']
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = None

    def get_queryset(self):
        return Banner.objects.all().order_by('-id')

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            # permission_classes = [permissions.IsAdminUser | IsSuperUser]
            permission_classes = [permissions.AllowAny]

        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class SizeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = SizeSerializer
    ordering_fields = ['created_at']

    filterset_class = SizeFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = None

    def get_queryset(self):
        qs = Size.objects.all().order_by('-id')
        
        
        if self.request.GET.get('id_list'):
            ids = str(self.request.GET.get('id_list'))
            id_list = list(map(int,ids.split(',')))
            qs = qs.filter(id__in = id_list)
        return qs

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            # permission_classes = [permissions.IsAdminUser | IsSuperUser]
            permission_classes = [permissions.AllowAny]

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
        queryset = self.filter_queryset(
            self.get_queryset().filter(product__is_active=True))

        page = self.paginate_queryset(queryset)
        if page is not None:
            sz = self.get_serializer(page, many=True)
            return self.get_paginated_response(sz.data)
        sz = self.get_serializer(queryset, many=True)
        return Response(sz.data)

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            # permission_classes = [IsSuperUser | permissions.IsAdminUser]
            permission_classes = [permissions.AllowAny]

        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all().order_by('-id')
    ordering_fields = ['created_at']
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['title', 'description']
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        qs = self.queryset.all()
        qs = self.filter_queryset(qs)
        size = self.request.GET.get('size')
        banner_discount = self.request.GET.get('banner_discount')
        product_type = self.request.GET.get('product_type') 

        
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max') 
        q_objects = Q()

        if price_min is not None:
            q_objects &= Q(uzs_price__gte=int(price_min))
        if price_max is not None:
            q_objects &= Q(uzs_price__lte=int(price_max))
        print(qs)
        print(q_objects)
        qs = qs.filter(q_objects)
        print(qs)
        if size:
            qs = qs.filter(size=size)
        if banner_discount:
            qs = qs.filter(banner_discount__title__icontains=banner_discount)
        if product_type:
            qs = qs.filter(product_type__icontains=product_type)
        
        return qs

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return ProductCreateSerializer
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
    

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
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
        product_type = sz_.data['product_type']
        errors = []
        for file in files:
            images[file] = []
            for i in files.getlist(file):
                sz = None
                if product_type == 'book':
                    sz = BookImageSerializer(data={'image': i, 'wrapper': str(file), 'product': sz_.data['id'],
                                                   'price': data[f'price_{str(file)}']})
                else:
                    sz = ProductImageCreateSerializer(data={'image': i, 'color': int(file), 'product': sz_.data['id'],
                                                            'price': data[f'price_{str(file)}']})
                sz.is_valid(raise_exception=True)
                sz.save()
                images[file].append(sz.data)
        return Response({'data': sz_.data, 'images': images, 'errors': errors}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def remove_image(self, request,pk = None):
        product = self.get_object()
        color = request.GET.get('color')
        wrapper = request.GET.get('wrapper')
        if wrapper:
            images = product.product_images.filter(wrapper = wrapper)
            images.delete()
        else:
            images = product.product_images.filter(color = color)
            images.delete()
        
        return Response({'data': 'removed'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def image_price(self, request,pk = None):
        product = self.get_object()
        data = request.data
        color =data.get('color',None)
        wrapper =data.get('wrapper',None)
        price =data.get('price',None)
        if wrapper:
            images = product.product_images.filter(wrapper = wrapper)
            images.update(price=price)
        else:
            images = product.product_images.filter(color = color)
            images.update(price=price)

        return Response({'data': 'updated'}, status=status.HTTP_200_OK)
    
    @action(methods=['get'],detail=True)
    def images(self, request, pk=None):
        product = self.get_object()
        images = product.product_images.all()
        product_images = []
        if images and product.product_type !='book':
            colors = set(images.values_list('color',flat=True))
            for i in colors:

                images_ = images.filter(color = i)
                price = images_.first().price
                color = images_.first().color
                sz = ProductImageSZ(images_,many=True)
              
                product_images.append({'color_id':color.id,'color_title':color.title,'price':price,'images':sz.data})
        elif images:
            wrappers = ('qattiq','yumshoq')
            for i in wrappers:
                images_ = images.filter(wrapper = i)
                if images_:
                    price = images_.first().price
                    sz = ProductImageSZ(images_,many=True)
                    product_images.append({'wrapper':i,'price':price,'images':sz.data})
        return Response({'product_type':product.product_type,'all_images':product_images})

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            # permission_classes = [IsSuperUser | permissions.IsAdminUser]
            permission_classes = [permissions.AllowAny]

        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class AdditionalInfoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                            mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = AdditionalInfoListSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
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
            # permission_classes = [IsSuperUser | permissions.IsAdminUser]
            permission_classes = [permissions.AllowAny]

        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class RateViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = RateListSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
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
            # permission_classes = [IsSuperUser | permissions.IsAdminUser]
            permission_classes = [permissions.AllowAny]

        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class AuthorModelViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthorSerializer
    pagination_class = LargeResultsSetPagination
