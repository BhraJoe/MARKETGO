from django.contrib import admin
from .models import Category, Favorite, Order, OrderItem, Product, ProductImage, Report, Review


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'category', 'price', 'location', 'active', 'created_at')
    list_filter = ('active', 'featured', 'category', 'condition')
    search_fields = ('name', 'description', 'seller__username', 'location')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]


admin.site.register(Category)
admin.site.register(Favorite)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Report)
