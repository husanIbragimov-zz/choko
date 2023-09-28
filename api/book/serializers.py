from apps.product.models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'icon', 'parent','is_active']

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

class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'wrapper', 'price', 'is_active']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'icon', 'parent']


class BookSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)
    tags  = TagSerializer(many=True, read_only=True)
    author = serializers.CharField(source='author.title', read_only=True)
    advertisement = serializers.CharField(source='advertisement.title', read_only=True)
    banner_discount = serializers.CharField(source='banner_discount.title', read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    product_images = serializers.ManyRelatedField(child_relation=BookImageSerializer(), read_only=True)


    def get_images(self, obj):
        return BookImageSerializer(obj.product_images.all(), many=True).data

    class Meta:
        model = Product
        fields = ['id', 'title','product_images', 'banner_discount', 'advertisement', 'status', 'category',
                  'author', 'description', 'images', 'availability', 'brand',
                  'percentage', 'discount', 'view', 'isbn', 'author', 'lang', 'script', 'total_pages',
                  'printed', 'format', 'year_of_creation', 'tags', 'product_type', 'created_at', 'updated_at', 'is_active']


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields  = ['id','title','author','description','isbn']

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'status', 'advertisement', 'banner_discount', 'brand', 
                  'percentage', 'description', 'availability', 'is_active']