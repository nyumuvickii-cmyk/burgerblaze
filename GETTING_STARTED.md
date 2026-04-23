# BurgerBlaze - Getting Started Guide

Welcome to **BurgerBlaze**, a complete online restaurant ordering system built with Django!

## 📋 Quick Overview

BurgerBlaze is a full-featured restaurant ordering platform with:

✅ **Complete Menu System** - Browse categorized items with images and prices  
✅ **Shopping Cart** - Add items, adjust quantities, view totals  
✅ **Order Management** - Place orders and track status  
✅ **Admin Dashboard** - Manage menu items and orders  
✅ **REST API** - Comprehensive API for integrations  
✅ **Modern Design** - Professional, responsive UI  
✅ **Production Ready** - Deploy to Render.com, Heroku, or DigitalOcean  

## 🚀 Quick Start (5 minutes)

### Option 1: Using Quick Start Script

```bash
cd /workspaces/burgerblaze
chmod +x quickstart.sh
./quickstart.sh
```

### Option 2: Manual Setup

```bash
# 1. Navigate to project
cd /workspaces/burgerblaze

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database
python manage.py migrate
python manage.py populate_menu

# 5. Create admin user
python manage.py createsuperuser

# 6. Collect static files
python manage.py collectstatic --noinput

# 7. Run server
python manage.py runserver
```

## 🌐 Accessing the Application

After starting the server:

- **Homepage**: http://localhost:8000
- **Menu**: http://localhost:8000/menu/
- **Checkout**: http://localhost:8000/order/
- **About**: http://localhost:8000/about/
- **Admin Panel**: http://localhost:8000/admin
  - Username: `admin`
  - Password: `admin123` (change after first login!)

## 📊 Admin Panel Guide

### Login
1. Go to http://localhost:8000/admin
2. Enter credentials (admin/admin123)

### Menu Management

**Add New Menu Item:**
1. Click "Menu Items" → "Add Menu Item"
2. Fill in details:
   - Name
   - Description
   - Category (Burgers, Sides, Drinks, Desserts)
   - Price
   - Upload image
   - Mark as available
   - Select dietary flags (Vegetarian, Spicy)
3. Click "Save"

**Categories:**
- Click "Menu Categories" to add/edit categories
- Reorder items with the "order" field

**Example: Adding Spicy Burger**
```
Name: Spicy Ghost Pepper Burger
Description: Flame-grilled beef with ghost peppers and scorching sauce
Category: Burgers
Price: $11.99
Image: [Upload ghost-pepper-burger.jpg]
Is Spicy: ✓ Check
Is Available: ✓ Check
```

### Order Management

**View Orders:**
1. Click "Orders" in admin
2. See all customer orders with status

**Update Order Status:**
1. Click on an order
2. Change status from dropdown:
   - **pending** → Order received
   - **confirmed** → Order approved
   - **preparing** → Being made
   - **ready** → Ready for pickup
   - **completed** → Delivered/picked up
   - **cancelled** → Order cancelled
3. Click "Save"

**Order Information:**
- Order number (auto-generated)
- Customer contact details
- Items ordered with quantities
- Special instructions
- Total price

## 🛒 How Customers Order

### Step 1: Browse Menu
- Visit homepage
- Click "Order Now" or "Menu"
- Browse items by category
- Filter by dietary needs

### Step 2: Add to Cart
- Click "+" button on item
- Item appears in cart (upper right)
- Adjust quantities in cart

### Step 3: Checkout
- Click cart icon
- Click "Checkout"
- Fill customer info:
  - Full name
  - Email
  - Phone number
  - Special requests
- Click "Place Order"
- Get order confirmation with order number

### Step 4: Track Order
- Check email or contact number
- Can query order by phone number
- See live status updates

## 📱 Frontend Features

### Homepage
- Hero section with call-to-action
- Feature highlights (quality, speed, variety)
- Today's specials showcase
- Quick access to menu

### Menu Page
- All items organized by category
- Filter by dietary preferences
- Search functionality
- One-click add to cart

### Shopping Cart
- Slide-out sidebar (top-right)
- Adjust quantities
- Remove items
- View running total
- Quick checkout button

### Order Page
- Order summary
- Customer information form
- Special instructions field
- Order confirmation with number

## 🔧 Configuration

### Environment Variables

Edit `.env`:

```bash
# Django
DEBUG=False (set to True for development)
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (leave empty for SQLite in dev)
DATABASE_URL=

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

### Static Files

Images go in:
- `/static/css/` - Stylesheets
- `/static/js/` - JavaScript files
- `/media/` - Menu item images (uploaded via admin)

### Categories

Default categories (can be modified):
- **Burgers** - Main course items
- **Sides** - Fries, salads, etc.
- **Drinks** - Beverages
- **Desserts** - Sweets and treats

## 🚀 Deploying to Production

### To Render.com (Recommended)

1. Push to GitHub
2. Go to render.com
3. Click "New Web Service"
4. Select your repository
5. Configure environment variables
6. Deploy!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed steps.

### To Heroku

1. `heroku login`
2. `heroku create your-app-name`
3. `git push heroku main`
4. `heroku run python manage.py migrate`
5. Done!

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete guide.

## 🗄️ Database Models

### MenuCategory
- Organizes menu items
- Has custom ordering
- Supports images and descriptions

### MenuItem
- Individual menu items
- Linked to categories
- Tracks price, availability, dietary info
- Stores images

### Order
- Customer orders
- Tracks status from pending to completed
- Records customer contact info
- Stores timestamps

### OrderItem
- Items within an order
- Quantity and price snapshot
- Special instructions per item

### Cart
- Session-based shopping carts
- Temporary storage before checkout
- Auto-cleans old carts

## 📡 API Quick Reference

### Get Menu Items
```bash
curl http://localhost:8000/api/menu/
```

### Create Order
```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "customer_phone": "555-1234",
    "items": [{"menu_item": 1, "quantity": 1}]
  }'
```

### Get Orders by Phone
```bash
curl http://localhost:8000/api/orders/by_phone/?phone=555-1234
```

See [API.md](API.md) for complete API documentation.

## 🐛 Troubleshooting

### Server won't start
```bash
# Check dependencies
pip install -r requirements.txt

# Check migrations
python manage.py migrate

# Reset database (careful!)
rm db.sqlite3
python manage.py migrate
python manage.py populate_menu
```

### Static files not loading
```bash
python manage.py collectstatic --noinput --clear
```

### Port 8000 already in use
```bash
python manage.py runserver 8001
```

### Database locked
```bash
# Delete temp database files
rm db.sqlite3-journal
```

## 📚 File Structure

```
burgerblaze/
├── manage.py                 # Django CLI
├── requirements.txt          # Dependencies
├── Procfile                  # Deployment config
├── render.yaml              # Render.com config
├── burgerblaze/
│   ├── settings.py          # Main config
│   ├── urls.py              # URL routes
│   └── ...
├── restaurant/              # Main app
│   ├── models.py            # Database models
│   ├── views.py             # API views
│   ├── admin.py             # Admin config
│   └── ...
├── templates/               # HTML pages
│   ├── base.html
│   ├── index.html
│   ├── menu.html
│   ├── order.html
│   └── about.html
├── static/
│   ├── css/style.css        # Main stylesheet
│   ├── js/main.js           # JavaScript
│   └── ...
└── README.md
```

## 🎨 Customization

### Change Theme Colors

Edit `static/css/style.css`:

```css
:root {
    --primary-color: #ff6b35;      /* Change to your orange */
    --secondary-color: #f7931e;    /* Change to your secondary color */
    --accent-color: #fdb913;       /* Change accent color */
    /* ... more colors ... */
}
```

### Add New Pages

1. Create template in `templates/`
2. Add view in `restaurant/views.py`
3. Add URL in `burgerblaze/urls.py`

### Add New Categories

1. Go to `/admin`
2. Click "Menu Categories" → "Add"
3. Fill in details
4. Save

## 👀 Key Features Explained

### Smart Cart Management
- Sessionless cart system
- Survives page refreshes
- Easy quantity updates
- One-click checkout

### Order Tracking
- Unique order numbers
- Status updates
- Phone-based lookup
- Email notifications (optional)

### Admin Dashboard
- Intuitive menu management
- Real-time order viewing
- Status update system
- Customer tracking

### Responsive Design
- Mobile-friendly
- Tablet optimized
- Desktop experience
- Touch-friendly buttons

## 🔐 Security

- CSRF protection enabled
- SQL injection prevention
- XSS protection with templates
- Secure password hashing
- Environment variable protection

## 📖 Learning Resources

- [Django Documentation](https://docs.djangoproject.com)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [HTML/CSS Guide](https://www.w3schools.com/)
- [JavaScript Basics](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)

## ❓ FAQ

**Q: Can I use images for menu items?**
A: Yes! Upload images via the admin panel for each menu item.

**Q: How do I change prices?**
A: Edit menu items in the admin panel and update the price field.

**Q: Can customers create accounts?**
A: Currently no - they order as guests. Can be added as a feature.

**Q: How are orders stored?**
A: In the PostgreSQL database (production) or SQLite (development).

**Q: Can I send email confirmations?**
A: Yes! Configure `EMAIL_BACKEND` in settings.py

**Q: Is data backed up?**
A: On cloud platforms (Render, Heroku), backups are automatic. Configure locally as needed.

## 🤝 Support

- Check [README.md](README.md) for general info
- See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help
- Review [API.md](API.md) for API questions
- Check error logs: `python manage.py runserver` output

## 🎉 You're Ready!

Your BurgerBlaze restaurant is ready to go! 

**Next Steps:**
1. Add your menu items
2. Customize branding/colors
3. Deploy to production
4. Start taking orders!

---

**Happy serving! 🔥**
