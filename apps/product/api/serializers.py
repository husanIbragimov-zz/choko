from rest_framework import serializers
from apps.product.models import Author, BannerDiscount, Currency, Advertisement, Category, Banner, Brand, Color, Size, \
    Product, ProductImage, AdditionalInfo, Rate


class AppBannerDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerDiscount
        fields = ('id', 'title', 'image', 'deadline', 'is_active', 'product_id')


class AppCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('id', 'amount')


class AppAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('id', 'icon', 'title', 'description', 'banner_image')


class AppCategoryChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'icon')


class AppCategoryParentSerializer(serializers.ModelSerializer):
    children = AppCategoryChildSerializer(many=True)

    def get_children(self, obj):
        qs = Category.objects.filter(parent=obj)  # .order_by("?")
        sz = AppCategoryChildSerializer(qs, many=True)
        return sz.data

    class Meta:
        model = Category
        fields = ('id', 'title', 'icon', 'children')


class AppBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'image')


class AppBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'title')


class AppColorAppSerializer(serializers.ModelSerializer):

    def get_name_display(self, obj):
        return obj.get_name_display()

    class Meta:
        model = Color
        fields = ('id', 'name', 'title', 'colored_name')


class AppSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('id', 'name')


class AppProductImageSerializer(serializers.ModelSerializer):
    color_title = serializers.CharField(source='color.title', read_only=True)
    color = serializers.CharField(source='color.name', read_only=True)


    class Meta:
        model = ProductImage
        fields = ('id', 'color_title', 'color', 'color', 'image', 'total_uzs')


class AppAdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInfo
        fields = ('id', 'title', 'description')


class AppRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ('id', 'user', 'rate', 'comment', 'rate_percent')


class AppAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name')


class AppProductSerializer(serializers.ModelSerializer):
    category = AppCategoryChildSerializer(many=True, read_only=True)
    product_images = AppProductImageSerializer(many=True, read_only=True)

    @staticmethod
    def get_status_display(obj):
        return obj.get_status_display()

    class Meta:
        model = Product
        fields = (
            'id', 'status', 'title', 'category', 'percentage', 'monthly_uzs', 'discount_uzs',
            'mid_rate_percent', 'product_images'
        )


class AppProductDetailSerializer(serializers.ModelSerializer):
    category = AppCategoryChildSerializer(many=True, read_only=True)
    brand = serializers.CharField(source='brand.title', read_only=True)
    size = AppSizeSerializer(many=True, read_only=True)
    product_images = AppProductImageSerializer(many=True, read_only=True)
    additional_info = AppAdditionalInfoSerializer(many=True, read_only=True)
    rate = AppRateSerializer(many=True, read_only=True)
    author = AppAuthorSerializer(read_only=True)

    @staticmethod
    def get_status_display(obj):
        return obj.get_status_display()

    class Meta:
        model = Product
        fields = (
            'id', 'status', 'title', 'category', 'brand', 'size', 'percentage',
            'discount', 'view', 'mid_rate_percent', 'description', 'availability', 'has_size', 'product_images',
            'additional_info', 'rate', 'author'
        )
