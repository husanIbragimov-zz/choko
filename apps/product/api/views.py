from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters
from rest_framework.decorators import action
from api.book.helper import LargeResultsSetPagination
from .filters import AppProductFilter
from apps.product.models import Product, ProductImage
from .serializers import AppProductSerializer, AppProductDetailSerializer


class AppProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = AppProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AppProductFilter
    search_fields = ['title', 'description']
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return AppProductSerializer
        elif self.action == 'retrieve':
            return AppProductDetailSerializer
        return AppProductSerializer
