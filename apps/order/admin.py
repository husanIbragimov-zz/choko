from django.contrib import admin

from apps.order.models import CartItem, Cart, Order, Wishlist


# Register your models here.

class CartItemAdmin(admin.TabularInline):
    model = CartItem
    list_display = ['id', "title", 'product', "description"]
    list_filter = ['prodcut', 'created_at']


class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemAdmin]
    list_display = ('session_id', 'variant', 'num_of_items', 'cart_total', 'completed',
                    'id')
    list_filter = ('completed', 'created_at')
    list_per_page = 20


class OrderAdmin(admin.ModelAdmin):
    inlines = [CartItemAdmin]
    list_display = ('user', 'num_of_items', 'cart_total', 'status',
                    'id')
    list_filter = ('status', 'created_at')
    list_per_page = 20


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'product',
                    'id',)
    list_filter = ('created_at',)
    list_per_page = 20


admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
