from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
import admin_thumbnails
from apps.product.forms import BannerFrom
from apps.product.models import Category, Brand, Banner, Product, ProductImage, Rate, Advertisement, Color, \
    AdditionalInfo


class BannerAdmin(admin.ModelAdmin):
    form = BannerFrom


@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ('id',)
    extra = 1


@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image', 'product', 'image_thumbnail']


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title', 'created_at', 'is_active', 'id')
    list_display_links = ('indented_title',)
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    list_per_page = 25


class ProductImageStackedInline(admin.StackedInline):
    model = ProductImage
    extra = 1


class AdditionalInfoAdmin(admin.TabularInline):
    model = AdditionalInfo
    list_display = ['id', "title", 'product', "description"]
    list_filter = ['prodcut', 'created_at']


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, AdditionalInfoAdmin]
    filter_horizontal = ('category',)
    list_display = ('image_tag',
                    'title', 'price', 'percentage', 'discount', 'get_discount_price', 'mid_rate', 'view', 'is_active',
                    'id')
    readonly_fields = ('mid_rate', 'get_discount_price',)
    list_filter = ('status', 'brand', 'updated_at', 'created_at')
    list_per_page = 20


admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(AdditionalInfo)
admin.site.register(Color)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Rate)
admin.site.register(Advertisement)
