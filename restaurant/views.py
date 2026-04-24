"""
Views for restaurant app API.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import MenuItem, MenuCategory, Order, OrderItem, Cart, CartItem
from .serializers import (
    MenuItemSerializer, MenuCategorySerializer, OrderSerializer, 
    CartSerializer, CartItemSerializer, OrderItemSerializer
)


def home_view(request):
    """Render home page."""
    return render(request, 'index.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('account')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('account')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required
def account_view(request):
    orders = request.user.orders.all().order_by('-created_at')
    return render(request, 'account.html', {'orders': orders})


class MenuViewSet(viewsets.ModelViewSet):
    """API endpoint for menu items."""
    queryset = MenuItem.objects.filter(is_available=True)
    serializer_class = MenuItemSerializer
    
    def get_queryset(self):
        queryset = MenuItem.objects.filter(is_available=True)
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__id=category)
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get menu items grouped by category."""
        categories = MenuCategory.objects.all()
        data = []
        for category in categories:
            items = MenuItem.objects.filter(category=category, is_available=True)
            data.append({
                'category': MenuCategorySerializer(category).data,
                'items': MenuItemSerializer(items, many=True).data
            })
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def specials(self, request):
        """Get specials (spicy items, vegetarian, etc.)."""
        items = MenuItem.objects.filter(is_available=True).all()
        spicy = items.filter(is_spicy=True)
        vegetarian = items.filter(is_vegetarian=True)
        return Response({
            'spicy': MenuItemSerializer(spicy, many=True).data,
            'vegetarian': MenuItemSerializer(vegetarian, many=True).data,
        })


class CategoryViewSet(viewsets.ModelViewSet):
    """API endpoint for menu categories."""
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer
    
    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """Get all items in a category."""
        category = self.get_object()
        items = MenuItem.objects.filter(category=category, is_available=True)
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    """API endpoint for orders."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new order from cart."""
        order_data = request.data
        
        # Create order
        customer_name = order_data.get('customer_name')
        customer_email = order_data.get('customer_email')
        if request.user.is_authenticated:
            customer_name = customer_name or request.user.get_full_name() or request.user.username
            customer_email = customer_email or request.user.email

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=order_data.get('customer_phone'),
            notes=order_data.get('notes', ''),
        )
        
        # Add items to order
        items_data = order_data.get('items', [])
        total = 0
        for item_data in items_data:
            menu_item = MenuItem.objects.get(id=item_data['menu_item'])
            quantity = item_data.get('quantity', 1)
            price = menu_item.price
            
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity,
                price=price,
                special_instructions=item_data.get('special_instructions', '')
            )
            total += price * quantity
        
        order.total_price = total
        order.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def by_phone(self, request):
        """Get orders by customer phone number."""
        phone = request.query_params.get('phone', None)
        if not phone:
            return Response({'error': 'Phone number required'}, status=status.HTTP_400_BAD_REQUEST)
        
        orders = Order.objects.filter(customer_phone=phone)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update order status."""
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return Response(OrderSerializer(order).data)
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)


class CartViewSet(viewsets.ModelViewSet):
    """API endpoint for shopping cart."""
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
    @action(detail=False, methods=['post'])
    def get_or_create(self, request):
        """Get or create cart for session."""
        session_id = request.data.get('session_id')
        if not session_id:
            return Response({'error': 'session_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart, created = Cart.objects.get_or_create(session_id=session_id)
        return Response(CartSerializer(cart).data)
    
    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """Add item to cart."""
        cart = self.get_object()
        menu_item_id = request.data.get('menu_item_id')
        quantity = request.data.get('quantity', 1)
        
        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                menu_item=menu_item,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return Response(CartSerializer(cart).data)
        except MenuItem.DoesNotExist:
            return Response({'error': 'Menu item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        """Remove item from cart."""
        cart = self.get_object()
        cart_item_id = request.data.get('cart_item_id')
        
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
            cart_item.delete()
            return Response(CartSerializer(cart).data)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def clear(self, request, pk=None):
        """Clear all items from cart."""
        cart = self.get_object()
        cart.items_list.all().delete()
        return Response(CartSerializer(cart).data)
