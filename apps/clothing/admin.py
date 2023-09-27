from django.contrib import admin
from .models import Tag, Clothing


class ClothingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'is_active')
    list_display_links = ('id', 'title')
    filter_horizontal = ('tags', 'size')
    list_editable = ('is_active',)
    search_fields = ('title', 'description')
    list_per_page = 25


admin.site.register(Tag)
admin.site.register(Clothing, ClothingAdmin)
