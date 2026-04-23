"""
Restaurant app models for burgerblaze.
"""
from django.db import models
from django.utils import timezone


class MenuCategory(models.Model):
    """Menu category like Burgers, Sides, Drinks, Desserts."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Menu Categories'
    
    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Menu items for the restaurant."""
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu-items/')
    is_available = models.BooleanField(default=True)
    is_vegetarian = models.BooleanField(default=False)
    is_spicy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name


class Order(models.Model):
    """Customer orders."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_number} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number: ORD-TIMESTAMP
            self.order_number = f"ORD-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Individual items in an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    special_instructions = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} in {self.order.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.menu_item.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    """Shopping cart for customers."""
    session_id = models.CharField(max_length=255, unique=True)
    items = models.ManyToManyField(MenuItem, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart {self.session_id}"
    
    def get_total(self):
        return sum(item.get_subtotal() for item in self.items_list.all())


class CartItem(models.Model):
    """Items in a cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items_list')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def get_subtotal(self):
        return self.menu_item.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"
