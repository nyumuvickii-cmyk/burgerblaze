"""
Tests for restaurant app models.
"""
from django.test import TestCase
from restaurant.models import MenuCategory, MenuItem, Order, OrderItem


class MenuCategoryTestCase(TestCase):
    def setUp(self):
        self.category = MenuCategory.objects.create(
            name='Burgers',
            description='Test burgers',
            order=1
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Burgers')
        self.assertEqual(str(self.category), 'Burgers')


class MenuItemTestCase(TestCase):
    def setUp(self):
        self.category = MenuCategory.objects.create(
            name='Burgers',
            order=1
        )
        self.item = MenuItem.objects.create(
            name='Test Burger',
            description='A test burger',
            category=self.category,
            price=9.99
        )

    def test_item_creation(self):
        self.assertEqual(self.item.name, 'Test Burger')
        self.assertEqual(float(self.item.price), 9.99)
        self.assertTrue(self.item.is_available)

    def test_item_string(self):
        self.assertEqual(str(self.item), 'Test Burger')


class OrderTestCase(TestCase):
    def setUp(self):
        self.category = MenuCategory.objects.create(
            name='Burgers',
            order=1
        )
        self.item = MenuItem.objects.create(
            name='Test Burger',
            description='A test burger',
            category=self.category,
            price=9.99
        )
        self.order = Order.objects.create(
            customer_name='John Doe',
            customer_email='john@example.com',
            customer_phone='123-456-7890'
        )

    def test_order_creation(self):
        self.assertEqual(self.order.customer_name, 'John Doe')
        self.assertTrue(self.order.order_number.startswith('ORD-'))

    def test_order_item_creation(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            menu_item=self.item,
            quantity=2
        )
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(float(order_item.price), 9.99)
