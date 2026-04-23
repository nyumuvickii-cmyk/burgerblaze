"""
Admin configuration for restaurant app.
"""
from django.contrib import admin
from .models import MenuCategory, MenuItem, Order, OrderItem, Cart, CartItem


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    ordering = ['order', 'name']
    fieldsets = (
        (None, {'fields': ('name', 'description', 'image', 'order')}),
    )


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'is_vegetarian', 'is_spicy']
    list_filter = ['category', 'is_available', 'is_vegetarian', 'is_spicy']
    search_fields = ['name', 'description']
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'description', 'category', 'price')}),
        ('Image', {'fields': ('image',)}),
        ('Attributes', {'fields': ('is_available', 'is_vegetarian', 'is_spicy')}),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'customer_name', 'customer_phone', 'customer_email']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Info', {'fields': ('order_number', 'status', 'created_at', 'updated_at')}),
        ('Customer Info', {'fields': ('customer_name', 'customer_email', 'customer_phone')}),
        ('Order Details', {'fields': ('total_price', 'notes')}),
    )
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Recalculate total
        obj.total_price = sum(item.price * item.quantity for item in obj.items.all())
        obj.save()


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'menu_item', 'quantity', 'get_subtotal']
    
    def get_subtotal(self, obj):
        return obj.get_subtotal()
    get_subtotal.short_description = 'Subtotal'
