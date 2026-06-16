from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Cart, CartItem, Order, OrderItem, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count']
    prepopulated_fields = {'slug': ('name',)}

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'product_name', 'quantity', 'price', 'subtotal']
    extra = 0

    def subtotal(self, obj):
        return f"₹{obj.subtotal}"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category',
        'price',
        'stock',
        'is_featured',
        'is_active',
        'created_at'
    ]

    list_filter = ['category', 'is_featured', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_featured', 'is_active']

    fields = [
        'name',
        'description',
        'category',
        'price',
        'stock',
        'image',
        'is_featured',
        'is_active'
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'full_name', 'email']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at', 'total_amount']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Info', {
            'fields': ('user', 'status', 'total_amount', 'notes', 'created_at', 'updated_at')
        }),
        ('Shipping Address', {
            'fields': ('full_name', 'email', 'phone', 'address', 'city', 'state', 'zip_code', 'country')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'country', 'created_at']
    search_fields = ['user__username', 'user__email']


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_items', 'total_price', 'created_at']
    inlines = [CartItemInline]

    def total_items(self, obj):
        return obj.total_items

    def total_price(self, obj):
        return f"₹{obj.total_price}"
