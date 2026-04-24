"""
Serializers for restaurant app.
"""
from rest_framework import serializers
from .models import MenuItem, MenuCategory, Order, OrderItem, Cart, CartItem


class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ['id', 'name', 'description', 'image']


class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'category', 'category_name', 'price', 
                  'image', 'is_available', 'is_vegetarian', 'is_spicy']


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'quantity', 'price', 'special_instructions']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'user', 'customer_name', 'customer_email', 'customer_phone',
                  'status', 'total_price', 'notes', 'items', 'created_at', 'updated_at']
        read_only_fields = ['order_number', 'created_at', 'updated_at']


class CartItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'menu_item', 'quantity', 'subtotal']
    
    def get_subtotal(self, obj):
        return float(obj.get_subtotal())


class CartSerializer(serializers.ModelSerializer):
    items_list = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'session_id', 'items_list', 'total', 'created_at']
    
    def get_total(self, obj):
        return float(obj.get_total())
