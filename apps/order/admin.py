from django.contrib import admin

from apps.order.models import CartItem, Cart


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


admin.site.register(Cart, CartAdmin)
