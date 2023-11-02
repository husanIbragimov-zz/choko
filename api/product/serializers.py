from django.db.models import Avg
from rest_framework import serializers
from apps.product.models import Author, Category, Brand, Color, Currency, BannerDiscount, Advertisement, Banner, Size, \
    ProductImage, Product, Rate, AdditionalInfo
from apps.base.models import Variant


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title_uz', 'title_ru', 'icon', 'parent']


class CategoryListSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()

    def get_icon(self, obj):
        if obj.icon:
            return obj.icon.url
        return ''

    class Meta:
        model = Category
        fields = ['id', 'title_uz', 'title_ru', 'icon', 'parent', 'children']

    @staticmethod
    def get_children(obj):
        return CategoryCreateSerializer(obj.children.all(), many=True).data


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title_uz', 'title_ru', 'product_type']


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
    deadline = serializers.DateField()

    class Meta:
        model = BannerDiscount
        fields = ['id', 'title', 'image', 'deadline', 'is_active']


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['id', 'icon', 'title_uz', 'title_ru', 'description_uz', 'description_ru', 'banner_image']


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'desc_uz', 'title_uz', 'desc_ru', 'title_ru', 'image']


class RateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['id', 'product', 'rate', 'user', 'comment']

    def validate(self, attrs):
        rate = attrs.get('rate')
        if rate < 1 or rate > 5:
            raise serializers.ValidationError('Rate must be between 1 and 5')
        return attrs


class RateListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    product = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = Rate
        fields = ['id', 'product_id', 'product', 'rate', 'user', 'comment']


class AdditionalInfoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInfo
        fields = ['id', 'product', 'title_uz', 'description_uz', 'title_ru', 'description_ru']


class AdditionalInfoListSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = AdditionalInfo
        fields = ['id', 'product', 'title_uz', 'description_uz', 'title_ru', 'description_ru']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class ProductListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.name', read_only=True)
    price_uzs = serializers.SerializerMethodField()
    discount_uzs = serializers.SerializerMethodField()
    brand_uz = serializers.CharField(source='brand.title_uz', read_only=True)
    brand_ru = serializers.CharField(source='brand.title_ru', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title_uz', 'title_ru', 'author', 'product_type', 'brand_uz', 'brand_ru', 'status',
                  'category', 'price_uzs', 'discount_uzs', 'is_active', 'language', 'yozuv']

    def validate(self, attrs):
        currency = Currency.objects.last()
        if currency is None:
            return serializers.ValidationError('Currency not found')
        return attrs

    @staticmethod
    def get_price_uzs(obj):
        if obj.product_images.first().price:
            return obj.product_images.first().price * Currency.objects.last().amount
        return 0

    @staticmethod
    def get_discount_uzs(obj):
        if obj.percentage:
            discount_sell = obj.product_images.first().price - (
                    obj.product_images.first().price * (obj.percentage / 100))
            return discount_sell * Currency.objects.last().amount
        return 0


class ProductImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'color', 'image', 'price']


class ProductImageListSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    product = serializers.CharField(source='product.title', read_only=True)
    color = serializers.CharField(source='color.name', read_only=True)

    class Meta:
        model = ProductImage
        fields = ['id', 'product_id', 'product', 'color', 'image', 'price']


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_type', 'author', 'title_uz', 'title_ru', 'category', 'status', 'advertisement',
                  'banner_discount', 'brand', 'size', 'percentage', 'description_uz', 'description_ru', 'language',
                  'yozuv', 'availability', 'has_size', 'is_active']


class ProductImagesSerializer(serializers.ModelSerializer):
    color = serializers.CharField(source='color.name', read_only=True)
    title = serializers.CharField(source='color.title', read_only=True)
    price_uzs = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'color', 'title', 'image', 'price', 'price_uzs']

    @staticmethod
    def get_price_uzs(obj):
        if obj.price:
            return obj.price * Currency.objects.last().amount
        return 0


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    brand_uz = serializers.CharField(source='brand.title_uz', read_only=True)
    brand_ru = serializers.CharField(source='brand.title_ru', read_only=True)
    size = SizeSerializer(many=True)
    mid_rate = serializers.SerializerMethodField()
    mid_rate_percent = serializers.SerializerMethodField()
    product_images = serializers.SerializerMethodField()
    price_uzs = serializers.SerializerMethodField()
    discount_uzs = serializers.SerializerMethodField()
    additional_info = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'product_type', 'title_uz', 'title_ru', 'brand_uz', 'category', 'brand_ru', 'size', 'percentage',
            'price_uzs', 'discount_uzs',
            'view', 'mid_rate', 'mid_rate_percent', 'availability', 'description_uz', 'description_ru',
            'product_images', 'additional_info', 'is_active', 'yozuv', 'advertisement', 'banner_discount', 'brand',
        ]

    def get_category(self, obj):
        return CategoryListSerializer(obj.category.all(), many=True).data

    @staticmethod
    def get_size(obj):
        return SizeSerializer(obj.size.all(), many=True).data

    @staticmethod
    def get_mid_rate(obj):
        result = Rate.objects.filter(
            product=obj.id).aggregate(avarage=Avg("rate"))
        if result['avarage']:
            return round(result['avarage'], 1)
        else:
            return 0.0

    @staticmethod
    def get_mid_rate_percent(obj):
        result = Rate.objects.filter(
            product=obj.id).aggregate(avarage=Avg("rate"))
        if result['avarage']:
            percent = result['avarage'] * 100 / 5
            return percent
        else:
            return 0.0

    @staticmethod
    def get_product_images(obj):
        return ProductImagesSerializer(obj.product_images.all(), many=True).data

    @staticmethod
    def get_price_uzs(obj):
        if obj.product_images.first().price:
            return obj.product_images.first().price * Currency.objects.last().amount
        return 0

    @staticmethod
    def get_discount_uzs(obj):
        if obj.percentage:
            discount_sell = obj.product_images.first().price - (
                    obj.product_images.first().price * (obj.percentage / 100))
            return discount_sell * Currency.objects.last().amount
        return 0

    @staticmethod
    def get_additional_info(obj):
        return AdditionalInfoListSerializer(obj.additional_info.all(), many=True).data
