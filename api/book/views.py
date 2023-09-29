from django.shortcuts import get_object_or_404
from api.book.helper import LargeResultsSetPagination
from apps.product.models import *
from .serializers import AuthorSerializer, BookCreateSerializer, BookImageSerializer, BookListSerializer, \
    BookSerializer
from rest_framework import mixins, status, viewsets, response, parsers
from rest_framework.decorators import action


class BookModelViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = BookSerializer
    pagination_class = LargeResultsSetPagination
    lookup_field = 'id'
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        elif self.action == 'retrieve':
            self.pagination_class = None
            return BookSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            self.pagination_class = None
            return BookCreateSerializer
        
        return BookSerializer
    

    def create(self, request, *args, **kwargs):
        data = request.data
        sz_ = BookCreateSerializer(data=data)
        sz_.is_valid(raise_exception=True)
        sz_.save()
        images = {

        }
        files = request.FILES
        for file in files:
            images[file] = []
            for i in files.getlist(file):
                sz = BookImageSerializer(data={'image': i, 'wrapper': str(file), 'product': sz_.data['id'],
                                               'price': data[f'price_{str(file)}']})
                sz.is_valid(raise_exception=True)
                sz.save()
                images[file].append(sz.data)

        return response.Response({'data': sz_.data, 'images': images}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=False)
    def remove_image(self, request):
        wrapper = request.GET.get('wrapper')
        product = request.GET.get('product')
        product = get_object_or_404(Product, id=product)
        images = ProductImage.objects.filter(wrapper=wrapper, product=product)
        images.delete()
        return response.Response({'data': 'removed'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=False)
    def image_price(self, request):
        wrapper = request.GET.get('wrapper')
        product = request.GET.get('product')
        price = request.GET.get('price')
        product = get_object_or_404(Product, id=product)
        images = ProductImage.objects.filter(wrapper=wrapper, product=product)
        images.update(price=price)
        return response.Response({'data': 'updated'}, status=status.HTTP_200_OK)


class ProductImageModelViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = BookImageSerializer
    lookup_field = 'id'


class AuthorModelViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'id'


