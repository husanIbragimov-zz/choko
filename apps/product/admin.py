from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from apps.product.forms import BannerFrom
from apps.product.models import Category, Brand, Banner, Tag, Product, ProductImage, Rate, Advertisement


class BannerAdmin(admin.ModelAdmin):
    form = BannerFrom


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


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageStackedInline]
    filter_horizontal = ('category', 'tags')
    list_display = (
        'title', 'price', 'percentage', 'discount', 'get_discount_price', 'mid_rate', 'view', 'is_active', 'id')
    readonly_fields = ('get_mid_rate', 'get_discount_price')
    list_filter = ('status', 'brand', 'updated_at', 'created_at')
    list_per_page = 20


admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Tag)
admin.site.register(Product, ProductAdmin)
admin.site.register(Rate)
admin.site.register(Advertisement)
