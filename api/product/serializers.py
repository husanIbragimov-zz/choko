from rest_framework import serializers
from apps.product.models import Category, Brand, Color, Currency, BannerDiscount, Advertisement


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
