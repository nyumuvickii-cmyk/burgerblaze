"""
Management command to populate initial restaurant data.
"""
from django.core.management.base import BaseCommand
from restaurant.models import MenuCategory, MenuItem


class Command(BaseCommand):
    help = 'Populate initial menu data for BurgerBlaze'

    def handle(self, *args, **options):
        # Check if data already exists
        if MenuCategory.objects.exists():
            self.stdout.write(self.style.WARNING('Menu data already exists. Skipping...'))
            return

        # Create categories
        categories_data = [
            {'name': 'Burgers', 'description': 'Our signature flame-grilled burgers', 'order': 1},
            {'name': 'Sides', 'description': 'Perfect accompaniments to your meal', 'order': 2},
            {'name': 'Drinks', 'description': 'Refreshing beverages', 'order': 3},
            {'name': 'Desserts', 'description': 'Sweet treats to finish your meal', 'order': 4},
        ]

        categories = {}
        for cat_data in categories_data:
            cat = MenuCategory.objects.create(**cat_data)
            categories[cat.name] = cat
            self.stdout.write(self.style.SUCCESS(f'Created category: {cat.name}'))

        # Create menu items
        burgers = [
            {
                'name': 'Classic Cheeseburger',
                'description': 'Flame-grilled beef patty with cheddar cheese, lettuce, tomato, and our special sauce',
                'category': categories['Burgers'],
                'price': 8.99,
                'is_vegetarian': False,
                'is_spicy': False,
            },
            {
                'name': 'Bacon Blaze Burger',
                'description': 'Double patty with crispy bacon, Swiss cheese, onions, and flame sauce',
                'category': categories['Burgers'],
                'price': 10.99,
                'is_vegetarian': False,
                'is_spicy': False,
            },
            {
                'name': 'Spicy Jalapeño Burger',
                'description': 'Beef patty with fresh jalapeños, pepper jack cheese, chipotle mayo',
                'category': categories['Burgers'],
                'price': 9.49,
                'is_vegetarian': False,
                'is_spicy': True,
            },
            {
                'name': 'Mushroom Swiss Burger',
                'description': 'Seasoned beef with sautéed mushrooms and melted Swiss cheese',
                'category': categories['Burgers'],
                'price': 9.99,
                'is_vegetarian': False,
                'is_spicy': False,
            },
            {
                'name': 'Veggie Blaze Burger',
                'description': 'Plant-based patty with fresh vegetables, vegan cheese, and special sauce',
                'category': categories['Burgers'],
                'price': 8.99,
                'is_vegetarian': True,
                'is_spicy': False,
            },
        ]

        sides = [
            {
                'name': 'Crispy Fries',
                'description': 'Golden crispy fries with sea salt',
                'category': categories['Sides'],
                'price': 3.49,
                'is_vegetarian': True,
                'is_spicy': False,
            },
            {
                'name': 'Spicy Cajun Fries',
                'description': 'Fries with Cajun spices and chipotle dipping sauce',
                'category': categories['Sides'],
                'price': 4.49,
                'is_vegetarian': True,
                'is_spicy': True,
            },
            {
                'name': 'Onion Rings',
                'description': 'Crispy battered onion rings with ranch dip',
                'category': categories['Sides'],
                'price': 4.99,
                'is_vegetarian': True,
                'is_spicy': False,
            },
            {
                'name': 'Garden Salad',
                'description': 'Fresh mixed greens with vegetables and choice of dressing',
                'category': categories['Sides'],
                'price': 5.99,
                'is_vegetarian': True,
                'is_spicy': False,
            },
        ]

        drinks = [
            {
                'name': 'Soft Drink',
                'description': 'Coca-Cola, Sprite, or Fanta - your choice of size',
                'category': categories['Drinks'],
                'price': 2.49,
                'is_vegetarian': True,
                'is_spicy': False,
            },
            {
                'name': 'Iced Tea',
                'description': 'Refreshing sweet or unsweet iced tea',
                'category': categories['Drinks'],
                'price': 2.49,
                'is_vegetarian': True,
                'is_spicy': False,
            },
            {
                'name': 'Milkshake',
                'description': 'Vanilla, chocolate, or strawberry thick shake',
                'category': categories['Drinks'],
                'price': 4.99,
                'is_vegetarian': True,
                'is_spicy': False,
            },
            {
                'name': 'Fresh Lemonade',
                'description': 'Freshly made lemonade - classic or strawberry',
                'category': categories['Drinks'],
                'price': 3.49,
                'is_vegetarian': True,
                'is_spicy': False,
            },
        ]

        desserts = [
            {
                'name': 'Chocolate Brownie',
                'description': 'Fudgy chocolate brownie with vanilla ice cream',
                'category': categories['Desserts'],
                'price': 5.99,
                'is_vegetarian': True,
                'is_spicy': False,
            },
            {
                'name': 'Ice Cream Sundae',
                'description': 'Vanilla ice cream with chocolate sauce, nuts, and whipped cream',
                'category': categories['Desserts'],
                'price': 4.99,
                'is_vegetarian': True,
                'is_spicy': False,
            },
            {
                'name': 'Apple Pie',
                'description': 'Warm apple pie with cinnamon and a scoop of ice cream',
                'category': categories['Desserts'],
                'price': 4.99,
                'is_vegetarian': True,
                'is_spicy': False,
            },
        ]

        all_items = burgers + sides + drinks + desserts
        for item_data in all_items:
            MenuItem.objects.create(**item_data)
            self.stdout.write(self.style.SUCCESS(f'Created menu item: {item_data["name"]}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated menu data!'))
