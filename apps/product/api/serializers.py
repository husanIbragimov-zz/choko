from rest_framework import serializers
from apps.product.models import BannerDiscount, Currency, Advertisement, Category, Banner, Brand, Color, Size, \
    Product, ProductImage, AdditionalInfo, Rate


class BannerDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerDiscount
        fields = ('id', 'title', 'image', 'deadline', 'is_active', 'product_id')


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('id', 'amount')


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('id', 'icon', 'title', 'description', 'banner_image')


class CategoryChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'icon')


class CategoryParentSerializer(serializers.ModelSerializer):
    children = CategoryChildSerializer(many=True)

    def get_children(self, obj):
        qs = Category.objects.filter(parent=obj)  # .order_by("?")
        sz = CategoryChildSerializer(qs, many=True)
        return sz.data

    class Meta:
        model = Category
        fields = ('id', 'title', 'icon', 'children')


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'image')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'title')


class ColorSerializer(serializers.ModelSerializer):

    def get_name_display(self, obj):
        return obj.get_name_display()

    class Meta:
        model = Color
        fields = ('id', 'name', 'title', 'colored_name')


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('id', 'name')


class ProductImageSerializer(serializers.ModelSerializer):
    color = ColorSerializer(many=True)

    class Meta:
        model = ProductImage
        fields = ('id', 'color', 'image', 'price', 'price_uzs', 'total_uzs')


class AdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInfo
        fields = ('id', 'title', 'description')


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ('id', 'user', 'rate', 'comment', 'rate_percent')


class ProductSerializer(serializers.ModelSerializer):
    banner_discount = BannerDiscountSerializer(read_only=True)
    advertisement = AdvertisementSerializer(read_only=True)
    category = CategoryChildSerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)
    size = SizeSerializer(many=True, read_only=True)

    def get_status_display(self, obj):
        return obj.get_status_display()

    class Meta:
        model = Product
        fields = (
            'id', 'banner_discount', 'advertisement', 'status', 'title', 'category', 'brand', 'size', 'percentage', 'discount', 'view', 'mid_rate_percent', 'description', 'availability', 'has_size'
        )
