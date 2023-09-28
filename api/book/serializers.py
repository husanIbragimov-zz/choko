from apps.product.models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'icon', 'parent', 'is_active']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class PrintedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printed
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']
        ref_name = 'Product Tag'


class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image', 'wrapper', 'price', 'is_active']


class BookSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.CharField(source='author.title', read_only=True)
    advertisement = serializers.CharField(source='advertisement.title', read_only=True)
    banner_discount = serializers.CharField(source='banner_discount.title', read_only=True)
    category = CategorySerializer(many=True, read_only=True)

    def get_images(self, obj):
        yumshoq = obj.product_images.filter(wrapper='yumshoq')
        qattiq = obj.product_images.filter(wrapper='qattiq')
        return {
            'yumshoq': BookImageSerializer(yumshoq, many=True).data,
            'qattiq': BookImageSerializer(qattiq, many=True).data
        }

    class Meta:
        model = Product
        fields = ['id', 'title', 'images', 'banner_discount', 'advertisement', 'status', 'category',
                  'author', 'description', 'availability', 'brand',
                  'percentage', 'discount', 'view', 'isbn', 'author', 'lang', 'script', 'total_pages',
                  'printed', 'format', 'year_of_creation', 'tags', 'product_type', 'created_at', 'updated_at',
                  'is_active']


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'author', 'description', 'isbn']


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'status', 'advertisement', 'banner_discount', 'brand',
                  'percentage', 'description', 'availability', 'is_active']
