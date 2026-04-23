# BurgerBlaze - Online Restaurant Ordering System

A full-featured Django + REST API restaurant ordering system with a modern, responsive frontend.

## Features

- **Menu Management**: Browse categorized menu items with filters
- **Shopping Cart**: Add items to cart with quantity management
- **Order Placement**: Complete checkout with customer information
- **Order Tracking**: Track orders by phone number
- **Admin Panel**: Manage menu items, categories, and orders
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Modern UI**: Clean, professional design inspired by contemporary restaurant sites
- **RESTful API**: Comprehensive API for all operations
- **Ready for Deployment**: Configured for Render.com and other platforms

## Technology Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite (dev), PostgreSQL (production)
- **Server**: Gunicorn + WhiteNoise
- **Deployment**: Render.com, Heroku-compatible

## Installation & Setup

### 1. Prerequisites

- Python 3.11+
- pip (Python package manager)
- Git

### 2. Clone and Setup Virtual Environment

```bash
# Navigate to the project
cd burgerblaze

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# Keep DEBUG=True for development
```

### 4. Initialize Database

```bash
# Apply migrations
python manage.py migrate

# Create superuser for admin panel
python manage.py createsuperuser

# Populate initial menu data
python manage.py populate_menu

# Collect static files
python manage.py collectstatic --noinput
```

### 5. Run Development Server

```bash
python manage.py runserver

# Server runs on http://localhost:8000
# Admin panel: http://localhost:8000/admin
```

## Project Structure

```
burgerblaze/
├── burgerblaze/              # Main Django project settings
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Main URL router
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── restaurant/              # Restaurant app
│   ├── models.py            # Database models
│   ├── views.py             # API views
│   ├── serializers.py       # DRF serializers
│   ├── admin.py             # Admin configuration
│   └── management/
│       └── commands/
│           └── populate_menu.py  # Initial data command
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── index.html          # Home page
│   ├── menu.html           # Menu page
│   ├── order.html          # Checkout page
│   └── about.html          # About page
├── static/                 # Static files
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   └── js/
│       └── main.js         # Main JavaScript
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── Procfile               # Deployment configuration
├── render.yaml            # Render.com configuration
└── .env.example           # Environment variables example
```

## API Endpoints

### Menu Endpoints
- `GET /api/menu/` - List all menu items
- `GET /api/menu/by_category/` - Get items grouped by category
- `GET /api/menu/specials/` - Get spicy and vegetarian items
- `GET /api/categories/` - List all categories

### Order Endpoints
- `POST /api/orders/` - Create new order
- `GET /api/orders/` - List all orders
- `GET /api/orders/by_phone/?phone=XXXXXXX` - Get orders by phone
- `PATCH /api/orders/{id}/update_status/` - Update order status

### Cart Endpoints
- `POST /api/cart/get_or_create/` - Get or create cart
- `POST /api/cart/{id}/add_item/` - Add item to cart
- `POST /api/cart/{id}/remove_item/` - Remove item from cart
- `POST /api/cart/{id}/clear/` - Clear cart

## Database Models

### MenuCategory
- name (CharField)
- description (TextField)
- image (ImageField)
- order (IntegerField)

### MenuItem
- name (CharField)
- description (TextField)
- category (ForeignKey)
- price (DecimalField)
- image (ImageField)
- is_available (BooleanField)
- is_vegetarian (BooleanField)
- is_spicy (BooleanField)

### Order
- order_number (CharField, unique)
- customer_name (CharField)
- customer_email (EmailField)
- customer_phone (CharField)
- status (CharField - pending, confirmed, preparing, ready, completed, cancelled)
- total_price (DecimalField)
- notes (TextField)
- created_at (DateTimeField)
- updated_at (DateTimeField)

### OrderItem
- order (ForeignKey)
- menu_item (ForeignKey)
- quantity (PositiveIntegerField)
- price (DecimalField)
- special_instructions (TextField)

### Cart
- session_id (CharField)
- created_at (DateTimeField)
- updated_at (DateTimeField)

## Admin Panel

Access the admin panel at `/admin/`:

1. **Menu Management**: Add, edit, or delete menu items and categories
2. **Order Management**: Review orders, update status, view order details
3. **Statistics**: Monitor order volume and popular items

## Deployment on Render.com

### 1. Push to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Connect to Render.com

1. Go to [render.com](https://render.com)
2. Sign in or create account
3. Click "New Web Service"
4. Connect your GitHub repository
5. Render will detect the `render.yaml` configuration

### 3. Configure Environment Variables

In Render.com dashboard:

1. Add these environment variables:
   - `DEBUG`: False
   - `SECRET_KEY`: Generate a random secure key
   - `ALLOWED_HOSTS`: your-domain.onrender.com

2. For PostgreSQL database:
   - Render will automatically create and connect DATABASE_URL

### 4. Deploy

```bash
# After connecting, Render will automatically:
# 1. Run migrations
# 2. Collect static files
# 3. Start the server
```

## Deployment on Heroku

### 1. Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Or download from https://devcenter.heroku.com/articles/heroku-cli
```

### 2. Deploy

```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-burgerblaze-app

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Populate data
heroku run python manage.py populate_menu

# View logs
heroku logs --tail
```

## Development Guide

### Adding New Menu Items

1. Via Admin Panel:
   - Go to `/admin/restaurant/menuitem/add/`
   - Fill in details
   - Upload image
   - Click Save

2. Via Django Shell:
```python
python manage.py shell
from restaurant.models import MenuItem, MenuCategory

category = MenuCategory.objects.get(name='Burgers')
MenuItem.objects.create(
    name='New Burger',
    description='Description here',
    category=category,
    price=9.99,
    is_available=True
)
```

### Customizing Styling

Edit `/static/css/style.css` to customize:
- Colors (CSS custom properties at the top)
- Layout and spacing
- Fonts and typography
- Responsive breakpoints

### Adding Features

1. Create models in `restaurant/models.py`
2. Create serializers in `restaurant/serializers.py`
3. Create views in `restaurant/views.py`
4. Register routes in `burgerblaze/urls.py`
5. Update admin configuration in `restaurant/admin.py`

## Frontend Features

### Homepage
- Hero section with call-to-action
- Feature highlights
- Today's specials display
- Call-to-action to view full menu

### Menu Page
- Browse all items by category
- Filter by dietary preferences (vegetarian, spicy)
- View item details (price, description, availability)
- Add items to cart with one click

### Shopping Cart
- Slide-out sidebar cart
- Adjust quantities
- Remove items
- View running total
- Proceed to checkout

### Checkout Page
- Order summary
- Customer information form
- Special instructions field
- Order confirmation with order number

### Order Tracking
- Track orders by phone number
- View order status in real-time
- See estimated time remaining

## Common Tasks

### Reset Database (Development)

```bash
# Delete db.sqlite3
rm db.sqlite3

# Re-run migrations
python manage.py migrate

# Create new superuser
python manage.py createsuperuser

# Populate menu data
python manage.py populate_menu
```

### Update Dependencies

```bash
# Update requirements.txt
pip list --outdated
pip install --upgrade package-name

# Update requirements.txt
pip freeze > requirements.txt
```

### Access Shell

```bash
python manage.py shell

# Example: Query menu items
from restaurant.models import MenuItem
items = MenuItem.objects.filter(is_available=True)
for item in items:
    print(item.name, item.price)
```

## Troubleshooting

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
```

### Database Errors

```bash
# Reset migrations (development only)
python manage.py migrate restaurant zero
python manage.py migrate
python manage.py populate_menu
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use

```bash
# Use different port
python manage.py runserver 8001
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Django and Django REST Framework documentation
3. Check Render.com documentation for deployment issues

## Future Enhancements

- User accounts and order history
- Advanced payment integration
- Real-time order notifications
- Kitchen dashboard for order management
- Email order confirmations
- Loyalty/rewards program
- Admin analytics dashboard
- Mobile app (React Native/Flutter)

---

**BurgerBlaze** - Serving the best burgers online! 🔥
