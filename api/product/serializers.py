from rest_framework import serializers
from apps.product.models import Category, Brand, Color, Currency, BannerDiscount, Advertisement, Banner, Size, \
    ProductImage, Product


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'icon', 'parent']


class CategoryListSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'icon', 'parent', 'children']

    @staticmethod
    def get_children(obj):
        return CategoryListSerializer(obj.children.all(), many=True).data


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'title']


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'amount']


class BannerDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerDiscount
        fields = ['id', 'title', 'image', 'deadline', 'is_active']


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['id', 'icon', 'title', 'description', 'banner_image']


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'desc', 'title', 'image']


class ProductListSerializer(serializers.ModelSerializer):
    banner_discount = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'discount', 'image']

    @staticmethod
    def get_banner_discount(obj):
        return BannerDiscountSerializer(obj.banner_discount.all(), many=True).data


class ProductImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'color', 'image', 'price']


class ProductImageListSerializer(serializers.ModelSerializer):
    color = serializers.CharField(source='color.name', read_only=True)

    class Meta:
        model = ProductImage
        fields = ['id', 'color', 'image', 'price']


